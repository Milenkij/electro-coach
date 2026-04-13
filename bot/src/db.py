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


async def save_message(session_id: UUID, role: str, content: str) -> None:
    pool = _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO messages (session_id, role, content)
            VALUES ($1, $2, $3)
            """,
            session_id,
            role,
            content,
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


async def decrement_free_sessions(user_id: int) -> None:
    pool = _get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE users
            SET free_sessions_left = free_sessions_left - 1
            WHERE id = $1 AND free_sessions_left > 0
            """,
            user_id,
        )
