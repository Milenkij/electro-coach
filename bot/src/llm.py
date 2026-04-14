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

_PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"

# Always-loaded layers (cached after first read)
_core_prompt: str | None = None

# Retrieval cards: keyword → filename
_CARD_KEYWORDS: dict[str, list[str]] = {
    "goal-pursuit": [
        "цель", "план", "приоритет", "фокус", "делать", "результат",
        "достичь", "стратегия", "действие", "обязательство",
    ],
    "self-esteem-and-self-trust": [
        "самооценка", "уверенность", "стыд", "самокритика", "неуверен",
        "обесценива", "недостаточно", "не заслуживаю", "самоуважение",
    ],
    "systems-thinking": [
        "повторяется", "опять", "цикл", "система", "хаос", "перегруз",
        "снова оказываюсь", "одно и то же", "петля",
    ],
    "self-sabotage-patterns": [
        "саботаж", "срыв", "снова делаю", "защита", "избегание",
        "разрушаю", "самосаботаж", "ловушка", "сценарий",
    ],
    "adhd-like-patterns": [
        "внимание", "прокрастинация", "запуск", "забываю", "хаос",
        "не могу начать", "отвлекаюсь", "время", "импульс", "гиперфокус",
    ],
}
_MAX_CARDS = 2  # load at most 2 cards per request

# Card content cache
_card_cache: dict[str, str] = {}


def _load_core_prompt() -> str:
    """Load and cache the always-loaded prompt layers."""
    global _core_prompt
    if _core_prompt is None:
        layers = [
            _PROMPTS_DIR / "base" / "base-identity.md",
            _PROMPTS_DIR / "base" / "safety-and-boundaries.md",
            _PROMPTS_DIR / "playbook" / "coach-playbook.md",
            _PROMPTS_DIR / "product-rules.md",
        ]
        parts = []
        for path in layers:
            parts.append(path.read_text(encoding="utf-8"))
        _core_prompt = "\n\n---\n\n".join(parts)
    return _core_prompt


def _load_card(name: str) -> str:
    """Load and cache a retrieval card by name."""
    if name not in _card_cache:
        path = _PROMPTS_DIR / "cards" / f"{name}.md"
        _card_cache[name] = path.read_text(encoding="utf-8")
    return _card_cache[name]


def _select_cards(messages: list[dict[str, str]]) -> list[str]:
    """Select relevant retrieval cards based on conversation keywords."""
    # Combine all user messages into searchable text
    text = " ".join(
        m["content"].lower() for m in messages if m["role"] == "user"
    )

    scores: dict[str, int] = {}
    for card_name, keywords in _CARD_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[card_name] = score

    # Return top N cards by score
    ranked = sorted(scores, key=scores.get, reverse=True)
    return ranked[:_MAX_CARDS]


def _build_system_prompt(
    messages: list[dict[str, str]] | None = None,
    session_started_at: datetime | None = None,
    time_budget: str | None = None,
) -> str:
    """Build system prompt from layers + conditional cards + session metadata."""
    prompt = _load_core_prompt()

    # Add relevant retrieval cards
    if messages:
        cards = _select_cards(messages)
        for card_name in cards:
            prompt += "\n\n---\n\n" + _load_card(card_name)
            logger.debug("Loaded card: %s", card_name)

    # Add session time metadata
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
    system_prompt = _build_system_prompt(messages, session_started_at, time_budget)

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
    system_prompt = _build_system_prompt(messages, session_started_at, time_budget)

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
