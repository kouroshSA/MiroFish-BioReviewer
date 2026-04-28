"""
LLM Client Wrapper
Unified OpenAI-format API calls
"""

import json
import re
import time
import threading
import logging
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config

logger = logging.getLogger('mirofish.llm_client')

# Module-level semaphore shared by all LLMClient instances so that
# concurrent requests across the entire process are throttled.
_llm_semaphore = threading.Semaphore(Config.MAX_CONCURRENT_LLM_REQUESTS)


# Hard ceiling for any single LLM call. Without this, the OpenAI SDK's
# default is 600s and a stalled provider can keep a Flask request handler
# tied up well past the user's patience. 120s is enough for the largest
# ontology / persona / report calls we make, while still surfacing dead
# providers quickly.
LLM_REQUEST_TIMEOUT_SECONDS = float(
    Config.LLM_API_KEY and getattr(Config, "LLM_TIMEOUT", 0) or 120.0
)


def _looks_like_anthropic(base_url: str) -> bool:
    """True for the OpenAI-compat layer at api.anthropic.com.

    Anthropic ignores `response_format`, so when we want JSON we have to
    rely on the system prompt. Detecting this lets `chat_json` add an
    explicit JSON-only suffix when calling Anthropic, while leaving
    OpenAI/Gemini/DeepSeek alone (they honor `response_format` natively).
    """
    return bool(base_url) and "anthropic.com" in base_url.lower()


class LLMClient:
    """LLM Client"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME
        self.timeout = timeout if timeout is not None else LLM_REQUEST_TIMEOUT_SECONDS

        if not self.api_key:
            raise ValueError("LLM_API_KEY not configured")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

        # Token usage tracking
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 4096,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Send a chat request

        Args:
            messages: List of messages
            temperature: Temperature parameter
            max_tokens: Maximum number of tokens
            response_format: Response format (e.g., JSON mode)

        Returns:
            Model response text
        """
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format:
            if (
                isinstance(response_format, dict)
                and response_format.get("type") == "json_object"
                and _looks_like_anthropic(self.base_url)
            ):
                # Anthropic's OpenAI-compat layer rejects
                # response_format={"type": "json_object"} with HTTP 400
                # ("response_format.type: Input should be 'json_schema'").
                # Strip the field — every prompt that asks for JSON also
                # asks for it in plain text in the system message, and
                # chat_json's fallback parser handles whatever markdown
                # wrapping Claude adds.
                logger.info(
                    "Dropping response_format=%s for Anthropic compat endpoint "
                    "(returns 400; falling back to prompt-only JSON instruction)",
                    response_format,
                )
            else:
                kwargs["response_format"] = response_format

        # INFO-level call lifecycle so the Colab log stream shows exactly
        # which calls are in flight and how long they take. Without this,
        # a hung LLM looked indistinguishable from a hung backend.
        approx_input_chars = sum(len(m.get("content", "")) for m in messages)
        logger.info(
            "LLM call ▶ model=%s base_url=%s ~%d input chars, max_tokens=%d, json_mode=%s",
            self.model, self.base_url, approx_input_chars, max_tokens,
            bool(response_format),
        )

        # Queue gate: limit concurrent LLM requests to avoid overwhelming
        # the inference server (Ollama/vLLM) and crashing the system.
        t0 = time.time()
        try:
            with _llm_semaphore:
                response = self.client.chat.completions.create(**kwargs)
        except Exception as e:
            logger.error(
                "LLM call ✗ FAILED after %.1fs: %s: %s",
                time.time() - t0, type(e).__name__, e,
            )
            raise
        dt = time.time() - t0

        # Track token usage
        pt = ct = 0
        if response.usage:
            pt = response.usage.prompt_tokens or 0
            ct = response.usage.completion_tokens or 0
            self.total_prompt_tokens += pt
            self.total_completion_tokens += ct
            self.total_tokens += pt + ct
        logger.info(
            "LLM call ✓ in %.1fs (prompt=%d, completion=%d)",
            dt, pt, ct,
        )

        content = response.choices[0].message.content
        if content is None:
            # Anthropic and some other providers return None content if the
            # request hit a content filter or finish_reason='content_filter'.
            # Treat as empty string so downstream code doesn't crash with
            # `TypeError: expected string or bytes-like object`.
            finish = getattr(response.choices[0], "finish_reason", "?")
            logger.warning("LLM returned None content (finish_reason=%s)", finish)
            return ""
        # Some models (e.g., MiniMax M2.5) include <think> reasoning content that needs to be removed
        content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
        return content

    def chat_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Send a chat request and return JSON

        Args:
            messages: List of messages
            temperature: Temperature parameter
            max_tokens: Maximum number of tokens

        Returns:
            Parsed JSON object
        """
        response = self.chat(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        # Clean up markdown code block markers
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\s*\n?', '', cleaned_response, flags=re.IGNORECASE)
        cleaned_response = re.sub(r'\n?```\s*$', '', cleaned_response)
        cleaned_response = cleaned_response.strip()

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            # Fallback: find the outermost balanced JSON object using brace counting.
            # This handles LLMs that append markdown after the JSON.
            extracted = self._extract_json_object(cleaned_response)
            if extracted:
                try:
                    return json.loads(extracted)
                except json.JSONDecodeError:
                    pass
            raise ValueError(f"Invalid JSON format returned by LLM: {cleaned_response}")

    @staticmethod
    def _extract_json_object(text: str) -> Optional[str]:
        """Extract the first balanced top-level JSON object from text."""
        start = text.find('{')
        if start == -1:
            return None
        depth = 0
        in_string = False
        escape = False
        for i in range(start, len(text)):
            ch = text[i]
            if escape:
                escape = False
                continue
            if ch == '\\' and in_string:
                escape = True
                continue
            if ch == '"' and not escape:
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    return text[start:i + 1]
        return None

    def get_usage_summary(self) -> Dict[str, int]:
        """Return accumulated token usage across all calls on this client."""
        return {
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_tokens,
        }
