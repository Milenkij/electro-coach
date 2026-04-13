import logging
from pathlib import Path

import httpx

from .config import config

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "prompt.md"
_system_prompt: str | None = None


def _load_system_prompt() -> str:
    global _system_prompt
    if _system_prompt is None:
        _system_prompt = _PROMPT_PATH.read_text(encoding="utf-8")
    return _system_prompt


async def chat(messages: list[dict[str, str]]) -> str:
    """Send messages to OpenRouter and return assistant response."""
    system_prompt = _load_system_prompt()

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
    return data["choices"][0]["message"]["content"]
