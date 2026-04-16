import logging
import re
from collections.abc import AsyncGenerator
from enum import Enum
from uuid import UUID

from . import db, llm

logger = logging.getLogger(__name__)


class UserState(str, Enum):
    IDLE = "idle"
    CHOOSING_MODE = "choosing_mode"
    COLLECTING_NAMES = "collecting_names"
    CONFIRMING_NAMES = "confirming_names"
    ACTIVE = "active"
    AWAITING_RATING = "awaiting_rating"


_SOLO_KEYWORDS = {"один", "одна", "сам", "сама", "solo", "1", "себя", "лично"}
_GROUP_KEYWORDS = {
    "несколько", "двое", "трое", "группа", "вместе", "команда",
    "два", "три", "четыре", "пять", "нас",
}
_CONFIRM_YES = {"да", "верно", "ок", "правильно", "ага", "угу", "yes", "точно", "всё верно"}
_CONFIRM_NO = {"нет", "не", "неверно", "неправильно", "no"}

# In-memory state per user (lost on restart — acceptable for MVP)
_user_states: dict[int, UserState] = {}
_user_sessions: dict[int, UUID] = {}
_user_participants: dict[int, list[str]] = {}


def cleanup_user(user_id: int) -> None:
    """Remove in-memory state for a user (e.g. after block)."""
    _user_states.pop(user_id, None)
    _user_sessions.pop(user_id, None)
    _user_participants.pop(user_id, None)


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
        participants = await db.get_session_participants(active["id"])
        if participants:
            _user_participants[user_id] = participants


PAYWALL_MESSAGE = (
    "Твой пробный период закончился.\n\n"
    "Чтобы продолжить работу с коучем, "
    "напиши @shapovalov_vsegda — обсудим подписку."
)


async def start_session(user_id: int, username: str | None, first_name: str) -> str:
    """Try to start a new coaching session. Returns response text."""
    await db.get_or_create_user(user_id, username, first_name)

    current = get_state(user_id)
    if current in (
        UserState.ACTIVE,
        UserState.CHOOSING_MODE,
        UserState.COLLECTING_NAMES,
        UserState.CONFIRMING_NAMES,
    ):
        return (
            "У тебя уже есть активная сессия. "
            "Продолжай диалог или заверши её командой /stop."
        )

    # Check subscription
    if not await db.is_subscription_active(user_id):
        return PAYWALL_MESSAGE

    # Create session immediately
    session = await db.create_session(user_id)
    _user_sessions[user_id] = session["id"]
    set_state(user_id, UserState.CHOOSING_MODE)

    return "Сессия будет на одного человека или на нескольких?"


def _parse_names(text: str) -> list[str]:
    """Parse participant names from free-form text."""
    text = text.strip()
    text = re.sub(r"\band\b", ",", text, flags=re.IGNORECASE)
    text = text.replace(" и ", ",")
    parts = re.split(r"[,\n;]+", text)
    names = []
    for part in parts:
        name = part.strip().strip(".-)")
        name = re.sub(r"^\d+[.)]\s*", "", name).strip()
        if name:
            names.append(name)
    return names


async def _handle_choosing_mode(user_id: int, text: str) -> str:
    words = set(text.lower().split())
    is_solo = bool(words & _SOLO_KEYWORDS)
    is_group = bool(words & _GROUP_KEYWORDS)

    if is_solo and not is_group:
        set_state(user_id, UserState.ACTIVE)
        return (
            "Отлично, работаем один на один.\n\n"
            "Расскажи, с чем пришёл сегодня — что хочешь разобрать или прояснить?"
        )

    if is_group and not is_solo:
        set_state(user_id, UserState.COLLECTING_NAMES)
        return "Перечисли имена участников."

    numbers = re.findall(r"\d+", text)
    for n in numbers:
        if int(n) > 1:
            set_state(user_id, UserState.COLLECTING_NAMES)
            return "Перечисли имена участников."

    return (
        "Не совсем понял. Сессия будет на одного человека или на нескольких? "
        "Напиши, например, «один» или «нас будет трое»."
    )


async def _handle_collecting_names(user_id: int, text: str) -> str:
    names = _parse_names(text)
    if not names:
        return "Не удалось разобрать имена. Перечисли участников через запятую."
    if len(names) < 2:
        return (
            "Для групповой сессии нужно минимум два участника. "
            "Перечисли имена через запятую."
        )

    _user_participants[user_id] = names
    set_state(user_id, UserState.CONFIRMING_NAMES)
    names_str = ", ".join(names)
    return f"Участники: {names_str}. Всё верно?"


async def _handle_confirming_names(user_id: int, text: str) -> str:
    lower = text.lower().strip()

    if lower in _CONFIRM_YES or lower.startswith("да"):
        participants = _user_participants.get(user_id, [])
        session_id = get_session_id(user_id)
        if session_id and participants:
            await db.set_session_participants(session_id, participants)
        set_state(user_id, UserState.ACTIVE)
        return (
            "Отлично! Начинаем групповую сессию.\n\n"
            "С чем вы пришли сегодня — что хотите разобрать или прояснить?"
        )

    if lower in _CONFIRM_NO or lower.startswith("нет"):
        set_state(user_id, UserState.COLLECTING_NAMES)
        return "Перечисли имена участников заново."

    names = _parse_names(text)
    if len(names) >= 2:
        _user_participants[user_id] = names
        names_str = ", ".join(names)
        return f"Участники: {names_str}. Всё верно?"

    return "Не совсем понял. Напиши «да», если участники верны, или перечисли имена заново."


async def handle_message(user_id: int, text: str) -> str:
    """Process a user message during an active session."""
    state = get_state(user_id)

    if state == UserState.CHOOSING_MODE:
        return await _handle_choosing_mode(user_id, text)
    if state == UserState.COLLECTING_NAMES:
        return await _handle_collecting_names(user_id, text)
    if state == UserState.CONFIRMING_NAMES:
        return await _handle_confirming_names(user_id, text)

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

    # Load session metadata
    meta = await db.get_session_meta(session_id)
    started_at = meta["started_at"] if meta else None
    time_budget = meta["time_budget"] if meta else None
    participants = _user_participants.get(user_id)

    # Get LLM response
    try:
        llm_response = await llm.chat(
            messages,
            session_started_at=started_at,
            time_budget=time_budget,
            participants=participants,
        )
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


async def handle_message_stream(user_id: int, text: str) -> AsyncGenerator[str, None]:
    """Process a user message with streaming. Yields accumulated text chunks.

    Raises RuntimeError for non-streaming errors (wrong state, no session).
    On LLM stream failure, falls back to non-streaming handle_message().
    """
    state = get_state(user_id)

    if state == UserState.CHOOSING_MODE:
        yield await _handle_choosing_mode(user_id, text)
        return
    if state == UserState.COLLECTING_NAMES:
        yield await _handle_collecting_names(user_id, text)
        return
    if state == UserState.CONFIRMING_NAMES:
        yield await _handle_confirming_names(user_id, text)
        return

    if state == UserState.AWAITING_RATING:
        yield await _handle_rating(user_id, text)
        return

    if state != UserState.ACTIVE:
        yield (
            "Сейчас нет активной сессии. "
            "Отправь /start или /new, чтобы начать."
        )
        return

    session_id = get_session_id(user_id)
    if session_id is None:
        set_state(user_id, UserState.IDLE)
        yield "Произошла ошибка. Отправь /new, чтобы начать новую сессию."
        return

    # Save user message
    await db.save_message(session_id, "user", text)

    # Build conversation history
    history = await db.get_session_messages(session_id)
    messages = [{"role": r["role"], "content": r["content"]} for r in history]

    # Load session metadata
    meta = await db.get_session_meta(session_id)
    started_at = meta["started_at"] if meta else None
    time_budget = meta["time_budget"] if meta else None
    participants = _user_participants.get(user_id)

    # Stream LLM response
    stream_state = llm.StreamState()
    try:
        async for accumulated_text in llm.chat_stream(
            messages,
            state=stream_state,
            session_started_at=started_at,
            time_budget=time_budget,
            participants=participants,
        ):
            yield accumulated_text
    except Exception:
        logger.exception("LLM stream error for user %s, falling back", user_id)
        # Fallback: non-streaming
        try:
            llm_response = await llm.chat(
                messages,
                session_started_at=started_at,
                time_budget=time_budget,
                participants=participants,
            )
        except Exception:
            logger.exception("LLM fallback error for user %s", user_id)
            yield "Произошла временная ошибка. Попробуй отправить сообщение ещё раз."
            return

        await db.save_message(
            session_id, "assistant", llm_response.content,
            prompt_tokens=llm_response.prompt_tokens,
            completion_tokens=llm_response.completion_tokens,
            cost=llm_response.cost,
        )
        yield llm_response.content
        return

    # Save assistant message with usage from stream
    if stream_state.response:
        r = stream_state.response
        await db.save_message(
            session_id, "assistant", r.content,
            prompt_tokens=r.prompt_tokens,
            completion_tokens=r.completion_tokens,
            cost=r.cost,
        )


async def stop_session(user_id: int) -> str:
    """Stop the current session and ask for a rating."""
    state = get_state(user_id)

    if state == UserState.AWAITING_RATING:
        return "Я уже жду твою оценку сессии от 1 до 10."

    if state not in (
        UserState.ACTIVE,
        UserState.CHOOSING_MODE,
        UserState.COLLECTING_NAMES,
        UserState.CONFIRMING_NAMES,
    ):
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

    # Clean up state
    set_state(user_id, UserState.IDLE)
    _user_sessions.pop(user_id, None)
    _user_participants.pop(user_id, None)

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
