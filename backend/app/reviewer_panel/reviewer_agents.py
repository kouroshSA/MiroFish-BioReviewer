"""
Reviewer agent invocation for MiroFish-BioReviewer.
Each reviewer is an independent LLM call with its own system prompt.
Called sequentially after simulation completes, before Reporter runs.

The runner is OpenAI-compatible-client friendly: it duck-types on a `client`
that exposes `chat.completions.create(...)`. The default plumbing in this
codebase is `app.utils.llm_client.LLMClient`, which the panel runner accepts
or constructs as needed.
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from .reviewer_prompts import (
    MECHANIST_SYSTEM_PROMPT,
    VISIONARY_SYSTEM_PROMPT,
    REALIST_SYSTEM_PROMPT,
    build_reviewer_user_prompt,
)

logger = logging.getLogger(__name__)


def _temp(env_name: str, default: float) -> float:
    raw = os.getenv(env_name)
    if raw is None or raw == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


REVIEWER_CONFIGS = [
    {
        "id": "mechanist",
        "name": "The Mechanist",
        "system_prompt": MECHANIST_SYSTEM_PROMPT,
        "temperature": _temp("REVIEWER_MECHANIST_TEMPERATURE", 0.3),
    },
    {
        "id": "visionary",
        "name": "The Visionary",
        "system_prompt": VISIONARY_SYSTEM_PROMPT,
        "temperature": _temp("REVIEWER_VISIONARY_TEMPERATURE", 0.7),
    },
    {
        "id": "realist",
        "name": "The Realist",
        "system_prompt": REALIST_SYSTEM_PROMPT,
        "temperature": _temp("REVIEWER_REALIST_TEMPERATURE", 0.4),
    },
]


def _strip_fences(raw: str) -> str:
    """Strip ```json fences a model may add despite instructions."""
    if not raw:
        return raw
    raw = raw.strip()
    if raw.startswith("```"):
        # ```json ... ``` or ``` ... ```
        body = raw.split("```")
        if len(body) >= 2:
            inner = body[1]
            if inner.startswith("json"):
                inner = inner[4:]
            raw = inner.strip()
    if raw.endswith("```"):
        raw = raw[: -3].strip()
    return raw


def _call_completion(client, model_name: str, messages, temperature: float, max_tokens: int) -> str:
    """
    Call an OpenAI-compatible chat-completions endpoint via duck typing.

    Supports two clients:
      - OpenAI SDK / LiteLLM (`client.chat.completions.create(...)`)
      - app.utils.llm_client.LLMClient (`client.chat(messages=..., temperature=..., max_tokens=...)`)
    """
    chat_attr = getattr(client, "chat", None)
    if chat_attr is not None and hasattr(chat_attr, "completions"):
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    # Fall back to the project's LLMClient interface
    if callable(getattr(client, "chat", None)):
        return client.chat(messages=messages, temperature=temperature, max_tokens=max_tokens) or ""
    raise TypeError(
        "Unsupported llm_client passed to reviewer_panel: expected OpenAI-style "
        "chat.completions.create or a callable .chat(messages=...) method."
    )


def run_reviewer_panel(
    proposal_text: str,
    simulation_posts: List[Dict[str, Any]],
    llm_client,
    model_name: str,
) -> List[Dict[str, Any]]:
    """
    Run all three reviewer agents and return their structured outputs.

    Args:
        proposal_text: Full text of the uploaded pre-proposal
        simulation_posts: List of post dicts from the swarm simulation
        llm_client: OpenAI-compatible client OR project's LLMClient
        model_name: LLM model name from environment config

    Returns:
        List of reviewer output dicts (parsed JSON from each reviewer)
    """
    if os.getenv("REVIEWER_PANEL_ENABLED", "true").lower() != "true":
        logger.info("Reviewer panel disabled via REVIEWER_PANEL_ENABLED=false")
        return []

    try:
        max_tokens = int(os.getenv("REVIEWER_MAX_TOKENS", "800"))
    except ValueError:
        max_tokens = 800

    user_prompt = build_reviewer_user_prompt(proposal_text, simulation_posts)
    results: List[Dict[str, Any]] = []

    for config in REVIEWER_CONFIGS:
        logger.info("Running reviewer: %s", config["name"])
        raw = ""
        try:
            raw = _call_completion(
                client=llm_client,
                model_name=model_name,
                messages=[
                    {"role": "system", "content": config["system_prompt"]},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=config["temperature"],
                max_tokens=max_tokens,
            )
            cleaned = _strip_fences(raw)
            parsed = json.loads(cleaned)
            parsed["reviewer_id"] = config["id"]
            results.append(parsed)
            logger.info(
                "Reviewer %s complete: %s",
                config["name"], parsed.get("recommendation", "N/A"),
            )
        except json.JSONDecodeError as e:
            logger.error("Reviewer %s returned invalid JSON: %s", config["name"], e)
            results.append({
                "reviewer_id": config["id"],
                "reviewer": config["name"],
                "error": f"JSON parse error: {str(e)}",
                "raw_response": raw,
            })
        except Exception as e:
            logger.error("Reviewer %s failed: %s", config["name"], e)
            results.append({
                "reviewer_id": config["id"],
                "reviewer": config["name"],
                "error": str(e),
            })

    return results
