"""
LLM Client Wrapper
Unified OpenAI-format API calls
"""

import json
import re
import threading
import logging
from typing import Optional, Dict, Any, List
from openai import OpenAI

from ..config import Config

logger = logging.getLogger('mirofish.llm_client')

# Module-level semaphore shared by all LLMClient instances so that
# concurrent requests across the entire process are throttled.
_llm_semaphore = threading.Semaphore(Config.MAX_CONCURRENT_LLM_REQUESTS)


class LLMClient:
    """LLM Client"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.api_key = api_key or Config.LLM_API_KEY
        self.base_url = base_url or Config.LLM_BASE_URL
        self.model = model or Config.LLM_MODEL_NAME

        if not self.api_key:
            raise ValueError("LLM_API_KEY not configured")

        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
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
            kwargs["response_format"] = response_format

        # Queue gate: limit concurrent LLM requests to avoid overwhelming
        # the inference server (Ollama/vLLM) and crashing the system.
        logger.debug("Waiting for LLM semaphore (%d/%d slots in use)",
                     Config.MAX_CONCURRENT_LLM_REQUESTS - _llm_semaphore._value,
                     Config.MAX_CONCURRENT_LLM_REQUESTS)
        with _llm_semaphore:
            response = self.client.chat.completions.create(**kwargs)

        # Track token usage
        if response.usage:
            pt = response.usage.prompt_tokens or 0
            ct = response.usage.completion_tokens or 0
            self.total_prompt_tokens += pt
            self.total_completion_tokens += ct
            self.total_tokens += pt + ct
            logger.debug("Tokens: prompt=%d, completion=%d (cumulative: %d)", pt, ct, self.total_tokens)

        content = response.choices[0].message.content
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
