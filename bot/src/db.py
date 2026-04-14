import logging
from uuid import UUID

import asyncpg

logger = logging.getLogger(__name__)

_pool: asyncpg.Pool | None = None


async def init_pool(database_url: str) -> None:
    global _pool
    _pool = await asyncpg.create_pool(database_url, min_size=2, max_size=10)
    logger.info("Database pool created")


async def close_pool() -> None:
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
        logger.info("Database pool closed")


def _get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_pool() first.")
    return _pool


async def run_migration(sql_path: str) -> None:
    pool = _get_pool()
    with open(sql_path) as f:
        sql = f.read()
    async with pool.acquire() as conn:
        await conn.execute(sql)
    logger.info("Migration applied: %s", sql_path)


async def get_or_create_user(
    user_id: int, username: str | None, first_name: str
) -> asyncpg.Record:
    pool = _get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
        if row is None:
            row = await conn.fetchrow(
                """
                INSERT INTO users (id, username, first_name)
                VALUES ($1, $2, $3)
                RETURNING *
                """,
                user_id,
                username,
                first_name,
            )
        return row


async def is_subscription_active(user_id: int) -> bool:
    """Check if user's subscription (or trial) is still active."""
    pool = _get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT subscription_until > NOW() AS active FROM users WHERE id = $1",
            user_id,
        )
        if row is None:
            return False
        return row["active"]


async def get_active_session(user_id: int) -> asyncpg.Record | None:
    pool = _get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT * FROM sessions WHERE user_id = $1 AND status = 'active'",
            user_id,
        )


async def create_session(user_id: int) -> asyncpg.Record:
    pool = _get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            """
            INSERT INTO sessions (user_id)
            VALUES ($1)
            RETURNING *
            """,
            user_id,
        )


async def complete_session(session_id: UUID) -> None:
    pool = _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE sessions
            SET status = 'completed', completed_at = NOW()
            WHERE id = $1
            """,
            session_id,
        )


async def rate_session(session_id: UUID, rating: int) -> None:
    pool = _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE sessions SET rating = $1 WHERE id = $2",
            rating,
            session_id,
        )


async def save_message(
    session_id: UUID,
    role: str,
    content: str,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    cost: object | None = None,
) -> None:
    pool = _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO messages (session_id, role, content, prompt_tokens, completion_tokens, cost)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            session_id,
            role,
            content,
            prompt_tokens,
            completion_tokens,
            cost,
        )
        await conn.execute(
            "UPDATE sessions SET message_count = message_count + 1 WHERE id = $1",
            session_id,
        )


async def get_session_messages(session_id: UUID) -> list[asyncpg.Record]:
    pool = _get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(
            """
            SELECT role, content FROM messages
            WHERE session_id = $1
            ORDER BY created_at ASC
            """,
            session_id,
        )


async def set_time_budget(session_id: UUID, time_budget: str) -> None:
    """Save user's stated time budget for the session."""
    pool = _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE sessions SET time_budget = $1 WHERE id = $2",
            time_budget,
            session_id,
        )


async def get_session_meta(session_id: UUID) -> asyncpg.Record | None:
    """Get session metadata for LLM context (started_at, time_budget)."""
    pool = _get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(
            "SELECT started_at, time_budget FROM sessions WHERE id = $1",
            session_id,
        )
