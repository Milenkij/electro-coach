import json
import logging
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import httpx

from .config import config


@dataclass(frozen=True)
class LLMResponse:
    content: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    cost: Decimal | None = None

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompt.md"
_system_prompt: str | None = None


def _load_system_prompt() -> str:
    global _system_prompt
    if _system_prompt is None:
        _system_prompt = _PROMPT_PATH.read_text(encoding="utf-8")
    return _system_prompt


def _build_system_prompt(
    session_started_at: datetime | None = None,
    time_budget: str | None = None,
) -> str:
    """Build system prompt with optional session time metadata."""
    prompt = _load_system_prompt()
    if session_started_at is not None:
        now = datetime.now(timezone.utc)
        meta = (
            "\n\n[Метаданные сессии]\n"
            f"Начало сессии: {session_started_at.strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"Текущее время: {now.strftime('%Y-%m-%d %H:%M UTC')}\n"
        )
        if time_budget:
            meta += f"Заявленное время пользователя: {time_budget}\n"
        else:
            meta += "Заявленное время пользователя: ещё не указано\n"
        prompt += meta
    return prompt


async def chat(
    messages: list[dict[str, str]],
    session_started_at: datetime | None = None,
    time_budget: str | None = None,
) -> LLMResponse:
    """Send messages to OpenRouter and return assistant response with usage."""
    system_prompt = _build_system_prompt(session_started_at, time_budget)

    payload = {
        "model": config.openrouter_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages,
        ],
    }

    headers = {
        "Authorization": f"Bearer {config.openrouter_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
        )

    if response.status_code != 200:
        logger.error("OpenRouter error %s: %s", response.status_code, response.text)
        raise RuntimeError(f"OpenRouter API error: {response.status_code}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]

    usage = data.get("usage") or {}
    prompt_tokens = usage.get("prompt_tokens")
    completion_tokens = usage.get("completion_tokens")
    raw_cost = usage.get("cost")
    cost = Decimal(str(raw_cost)) if raw_cost is not None else None

    return LLMResponse(
        content=content,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        cost=cost,
    )


@dataclass
class StreamState:
    """Mutable accumulator for streaming — holds final LLMResponse after iteration."""
    response: LLMResponse | None = None


async def chat_stream(
    messages: list[dict[str, str]],
    state: StreamState | None = None,
    session_started_at: datetime | None = None,
    time_budget: str | None = None,
) -> AsyncGenerator[str, None]:
    """Stream LLM response via SSE. Yields accumulated text on each chunk.

    After iteration completes, state.response contains the final LLMResponse
    with content and usage data.
    """
    system_prompt = _build_system_prompt(session_started_at, time_budget)

    payload = {
        "model": config.openrouter_model,
        "stream": True,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages,
        ],
    }

    headers = {
        "Authorization": f"Bearer {config.openrouter_api_key}",
        "Content-Type": "application/json",
    }

    accumulated = ""
    usage_data: dict = {}

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers,
        ) as response:
            if response.status_code != 200:
                body = await response.aread()
                logger.error("OpenRouter stream error %s: %s", response.status_code, body.decode())
                raise RuntimeError(f"OpenRouter API error: {response.status_code}")

            async for line in response.aiter_lines():
                if not line.startswith("data: "):
                    continue

                data_str = line[6:]
                if data_str.strip() == "[DONE]":
                    break

                try:
                    chunk = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                # Accumulate content
                choices = chunk.get("choices") or []
                if choices:
                    delta = choices[0].get("delta") or {}
                    content = delta.get("content")
                    if content:
                        accumulated += content
                        yield accumulated

                # Capture usage from last chunk
                if "usage" in chunk:
                    usage_data = chunk["usage"]

    prompt_tokens = usage_data.get("prompt_tokens")
    completion_tokens = usage_data.get("completion_tokens")
    raw_cost = usage_data.get("cost")
    cost = Decimal(str(raw_cost)) if raw_cost is not None else None

    if state is not None:
        state.response = LLMResponse(
            content=accumulated,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost,
        )
