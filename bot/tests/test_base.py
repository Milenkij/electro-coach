"""10 базовых тестов ElectroCoach bot — запускать после каждого инкремента версии."""

import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Fixtures & helpers
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _reset_session_state():
    """Reset in-memory session state between tests."""
    from src.session import _user_sessions, _user_states

    _user_states.clear()
    _user_sessions.clear()


def _make_user_record(subscription_until=None, **overrides):
    """Create a fake asyncpg.Record-like dict for users table."""
    if subscription_until is None:
        subscription_until = datetime.now(timezone.utc) + timedelta(hours=72)
    record = {
        "id": 123,
        "username": "testuser",
        "first_name": "Test",
        "subscription_until": subscription_until,
        "created_at": datetime.now(timezone.utc),
    }
    record.update(overrides)
    return record


def _make_session_record(**overrides):
    from uuid import uuid4

    record = {
        "id": uuid4(),
        "user_id": 123,
        "status": "active",
        "started_at": datetime.now(timezone.utc),
        "completed_at": None,
        "rating": None,
        "message_count": 0,
        "time_budget": None,
    }
    record.update(overrides)
    return record


# ---------------------------------------------------------------------------
# Test 1: System prompt loads successfully
# ---------------------------------------------------------------------------


def test_system_prompt_loads():
    """prompt.md exists and is non-empty."""
    from src.llm import _load_system_prompt

    prompt = _load_system_prompt()
    assert len(prompt) > 100
    assert "GROW" in prompt


# ---------------------------------------------------------------------------
# Test 2: System prompt includes timing metadata when provided
# ---------------------------------------------------------------------------


def test_system_prompt_with_time_metadata():
    """_build_system_prompt injects session metadata."""
    from src.llm import _build_system_prompt

    started = datetime(2026, 4, 14, 12, 0, tzinfo=timezone.utc)
    prompt = _build_system_prompt(session_started_at=started, time_budget="30 минут")
    assert "[Метаданные сессии]" in prompt
    assert "30 минут" in prompt
    assert "2026-04-14 12:00 UTC" in prompt


# ---------------------------------------------------------------------------
# Test 3: System prompt without time metadata has no metadata block
# ---------------------------------------------------------------------------


def test_system_prompt_no_metadata():
    """Without session args, no metadata block is appended."""
    from src.llm import _build_system_prompt

    prompt = _build_system_prompt()
    assert "[Метаданные сессии]" not in prompt


# ---------------------------------------------------------------------------
# Test 4: Start session — active subscription
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_start_session_active_subscription():
    """User with active subscription can start a session."""
    from src import session

    user = _make_user_record()
    sess = _make_session_record()

    with (
        patch("src.session.db.get_or_create_user", new_callable=AsyncMock, return_value=user),
        patch("src.session.db.is_subscription_active", new_callable=AsyncMock, return_value=True),
        patch("src.session.db.create_session", new_callable=AsyncMock, return_value=sess),
    ):
        result = await session.start_session(123, "testuser", "Test")

    assert "Сессия началась" in result
    assert session.get_state(123) == session.UserState.ACTIVE


# ---------------------------------------------------------------------------
# Test 5: Start session — expired subscription (paywall)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_start_session_expired_subscription():
    """User with expired subscription gets paywall message."""
    from src import session

    user = _make_user_record(
        subscription_until=datetime.now(timezone.utc) - timedelta(hours=1)
    )

    with (
        patch("src.session.db.get_or_create_user", new_callable=AsyncMock, return_value=user),
        patch("src.session.db.is_subscription_active", new_callable=AsyncMock, return_value=False),
    ):
        result = await session.start_session(123, "testuser", "Test")

    assert "@shapovalov_vsegda" in result
    assert session.get_state(123) == session.UserState.IDLE


# ---------------------------------------------------------------------------
# Test 6: Cannot start two sessions simultaneously
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_double_session_blocked():
    """Starting a second session while one is active returns warning."""
    from src import session

    user = _make_user_record()
    sess = _make_session_record()

    with (
        patch("src.session.db.get_or_create_user", new_callable=AsyncMock, return_value=user),
        patch("src.session.db.is_subscription_active", new_callable=AsyncMock, return_value=True),
        patch("src.session.db.create_session", new_callable=AsyncMock, return_value=sess),
    ):
        await session.start_session(123, "testuser", "Test")
        result = await session.start_session(123, "testuser", "Test")

    assert "уже есть активная сессия" in result


# ---------------------------------------------------------------------------
# Test 7: Stop session transitions to AWAITING_RATING
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_stop_session_asks_for_rating():
    """Stopping a session moves user to AWAITING_RATING state."""
    from src import session

    user = _make_user_record()
    sess = _make_session_record()

    with (
        patch("src.session.db.get_or_create_user", new_callable=AsyncMock, return_value=user),
        patch("src.session.db.is_subscription_active", new_callable=AsyncMock, return_value=True),
        patch("src.session.db.create_session", new_callable=AsyncMock, return_value=sess),
        patch("src.session.db.complete_session", new_callable=AsyncMock),
    ):
        await session.start_session(123, "testuser", "Test")
        result = await session.stop_session(123)

    assert "от 1 до 10" in result
    assert session.get_state(123) == session.UserState.AWAITING_RATING


# ---------------------------------------------------------------------------
# Test 8: Rating is saved and state resets to IDLE
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_rating_saves_and_resets_state():
    """After submitting rating, state goes back to IDLE."""
    from src import session

    user = _make_user_record()
    sess = _make_session_record()

    with (
        patch("src.session.db.get_or_create_user", new_callable=AsyncMock, return_value=user),
        patch("src.session.db.is_subscription_active", new_callable=AsyncMock, return_value=True),
        patch("src.session.db.create_session", new_callable=AsyncMock, return_value=sess),
        patch("src.session.db.complete_session", new_callable=AsyncMock),
        patch("src.session.db.rate_session", new_callable=AsyncMock) as mock_rate,
    ):
        await session.start_session(123, "testuser", "Test")
        await session.stop_session(123)
        result = await session.handle_message(123, "8")

    mock_rate.assert_called_once_with(sess["id"], 8)
    assert session.get_state(123) == session.UserState.IDLE
    assert "8/10" in result


# ---------------------------------------------------------------------------
# Test 9: Invalid rating is rejected
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_invalid_rating_rejected():
    """Non-numeric or out-of-range rating is rejected."""
    from src import session

    user = _make_user_record()
    sess = _make_session_record()

    with (
        patch("src.session.db.get_or_create_user", new_callable=AsyncMock, return_value=user),
        patch("src.session.db.is_subscription_active", new_callable=AsyncMock, return_value=True),
        patch("src.session.db.create_session", new_callable=AsyncMock, return_value=sess),
        patch("src.session.db.complete_session", new_callable=AsyncMock),
    ):
        await session.start_session(123, "testuser", "Test")
        await session.stop_session(123)

        result = await session.handle_message(123, "abc")
        assert "от 1 до 10" in result

        result = await session.handle_message(123, "15")
        assert "от 1 до 10" in result

    assert session.get_state(123) == session.UserState.AWAITING_RATING


# ---------------------------------------------------------------------------
# Test 10: Message without active session prompts to start
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_message_without_session():
    """Sending a message in IDLE state suggests /start or /new."""
    from src import session

    result = await session.handle_message(123, "привет")
    assert "/start" in result or "/new" in result
