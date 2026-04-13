import logging
from enum import Enum
from uuid import UUID

from . import db, llm

logger = logging.getLogger(__name__)


class UserState(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"
    AWAITING_RATING = "awaiting_rating"


# In-memory state per user (lost on restart — acceptable for MVP)
_user_states: dict[int, UserState] = {}
_user_sessions: dict[int, UUID] = {}


def cleanup_user(user_id: int) -> None:
    """Remove in-memory state for a user (e.g. after block)."""
    _user_states.pop(user_id, None)
    _user_sessions.pop(user_id, None)


def get_state(user_id: int) -> UserState:
    return _user_states.get(user_id, UserState.IDLE)


def set_state(user_id: int, state: UserState) -> None:
    _user_states[user_id] = state


def get_session_id(user_id: int) -> UUID | None:
    return _user_sessions.get(user_id)


async def restore_state(user_id: int) -> None:
    """Restore user state from DB (e.g. after bot restart)."""
    active = await db.get_active_session(user_id)
    if active:
        _user_states[user_id] = UserState.ACTIVE
        _user_sessions[user_id] = active["id"]


async def start_session(user_id: int, username: str | None, first_name: str) -> str:
    """Try to start a new coaching session. Returns response text."""
    user = await db.get_or_create_user(user_id, username, first_name)

    # Check if already in a session
    if get_state(user_id) == UserState.ACTIVE:
        return (
            "У тебя уже есть активная сессия. "
            "Продолжай диалог или заверши её командой /stop."
        )

    # Check free sessions limit
    if not user["is_subscribed"] and user["free_sessions_left"] <= 0:
        return (
            "Твои бесплатные сессии закончились.\n\n"
            "Чтобы продолжить работу с коучем, "
            "напиши нам для оформления подписки: @electrocoach_support"
        )

    # Create session
    session = await db.create_session(user_id)
    _user_sessions[user_id] = session["id"]
    set_state(user_id, UserState.ACTIVE)

    return (
        "Сессия началась. Расскажи, с чем пришёл сегодня — "
        "что хочешь разобрать или прояснить?"
    )


async def handle_message(user_id: int, text: str) -> str:
    """Process a user message during an active session."""
    state = get_state(user_id)

    if state == UserState.AWAITING_RATING:
        return await _handle_rating(user_id, text)

    if state != UserState.ACTIVE:
        return (
            "Сейчас нет активной сессии. "
            "Отправь /start или /new, чтобы начать."
        )

    session_id = get_session_id(user_id)
    if session_id is None:
        set_state(user_id, UserState.IDLE)
        return "Произошла ошибка. Отправь /new, чтобы начать новую сессию."

    # Save user message
    await db.save_message(session_id, "user", text)

    # Build conversation history
    history = await db.get_session_messages(session_id)
    messages = [{"role": r["role"], "content": r["content"]} for r in history]

    # Get LLM response
    try:
        llm_response = await llm.chat(messages)
    except Exception:
        logger.exception("LLM error for user %s", user_id)
        return (
            "Произошла временная ошибка. Попробуй отправить сообщение ещё раз."
        )

    # Save assistant message with usage
    await db.save_message(
        session_id,
        "assistant",
        llm_response.content,
        prompt_tokens=llm_response.prompt_tokens,
        completion_tokens=llm_response.completion_tokens,
        cost=llm_response.cost,
    )

    return llm_response.content


async def stop_session(user_id: int) -> str:
    """Stop the current session and ask for a rating."""
    state = get_state(user_id)

    if state == UserState.AWAITING_RATING:
        return "Я уже жду твою оценку сессии от 1 до 10."

    if state != UserState.ACTIVE:
        return "Нет активной сессии для завершения."

    session_id = get_session_id(user_id)
    if session_id:
        await db.complete_session(session_id)

    set_state(user_id, UserState.AWAITING_RATING)

    return (
        "Сессия завершена. Спасибо за работу!\n\n"
        "Оцени сессию от 1 до 10, где:\n"
        "1 — совсем не помогло\n"
        "10 — получил полную ясность и конкретный шаг\n\n"
        "Просто отправь число."
    )


async def _handle_rating(user_id: int, text: str) -> str:
    """Process session rating."""
    text = text.strip()

    try:
        rating = int(text)
    except ValueError:
        return "Отправь число от 1 до 10."

    if rating < 1 or rating > 10:
        return "Оценка должна быть от 1 до 10."

    session_id = get_session_id(user_id)
    if session_id:
        await db.rate_session(session_id, rating)
        await db.decrement_free_sessions(user_id)

    # Clean up state
    set_state(user_id, UserState.IDLE)
    _user_sessions.pop(user_id, None)

    if rating >= 7:
        return (
            f"Спасибо за оценку {rating}/10! Рад, что сессия была полезной. "
            "Когда будешь готов к следующей — отправь /new."
        )
    else:
        return (
            f"Спасибо за оценку {rating}/10 и честную обратную связь. "
            "Я учусь быть полезнее. Когда будешь готов — отправь /new."
        )
