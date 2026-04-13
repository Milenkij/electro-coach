import logging
import time

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ChatAction, ChatMemberStatus, ParseMode
from aiogram.filters import Command
from aiogram.methods import SendMessageDraft

from . import session
from .formatting import md_to_tg_html

DRAFT_THROTTLE = 0.3  # seconds between draft updates

logger = logging.getLogger(__name__)

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    user = message.from_user
    if user is None:
        return

    await message.answer(
        "Привет! Я — AI-коуч. Помогаю разобраться с тем, что мешает двигаться вперёд, "
        "и выйти из разговора с конкретным первым шагом.\n\n"
        "Формат: одна сессия = один запрос → структурированный диалог → твой следующий шаг.\n\n"
        "Каждая сессия начинается с чистого листа.\n\n"
        "Команды:\n"
        "/new — начать новую сессию\n"
        "/stop — завершить текущую сессию"
    )

    # Restore state from DB (e.g. after restart)
    await session.restore_state(user.id)

    # Auto-start first session if idle
    if session.get_state(user.id) == session.UserState.IDLE:
        response = await session.start_session(
            user.id, user.username, user.first_name or "User"
        )
        await message.answer(response)


@router.message(Command("new"))
async def cmd_new(message: types.Message) -> None:
    user = message.from_user
    if user is None:
        return

    response = await session.start_session(
        user.id, user.username, user.first_name or "User"
    )
    await message.answer(response)


@router.message(Command("stop"))
async def cmd_stop(message: types.Message) -> None:
    user = message.from_user
    if user is None:
        return

    response = await session.stop_session(user.id)
    await message.answer(response)


@router.my_chat_member()
async def handle_chat_member(update: types.ChatMemberUpdated) -> None:
    """Handle block/unblock — just log, prevent update queue from stalling."""
    status = update.new_chat_member.status
    user_id = update.from_user.id
    logger.info("Chat member update: user %s → %s", user_id, status)
    if status in (ChatMemberStatus.KICKED, ChatMemberStatus.LEFT):
        # User blocked the bot — clean up in-memory state
        session.cleanup_user(user_id)


@router.message()
async def handle_text(message: types.Message) -> None:
    user = message.from_user
    if user is None:
        return

    if not message.text:
        await message.answer(
            "Пока я работаю только с текстом. Напиши словами — так я смогу помочь."
        )
        return

    # Restore state if needed (bot might have restarted)
    if session.get_state(user.id) == session.UserState.IDLE:
        await session.restore_state(user.id)

    logger.info("User %s: %s", user.id, message.text)

    bot = message.bot
    chat_id = message.chat.id

    # Try streaming
    draft_id = int(time.time() * 1000) % 2147483647
    last_draft_ts = 0.0
    final_text = ""
    streamed = False
    thinking_msg: types.Message | None = None

    try:
        # Immediate feedback — regular message, will be deleted when stream starts
        thinking_msg = await message.answer("Думаю...")

        async for accumulated_text in session.handle_message_stream(user.id, message.text):
            # Delete "Думаю..." on first chunk
            if thinking_msg is not None:
                try:
                    await thinking_msg.delete()
                except Exception:
                    pass
                thinking_msg = None

            final_text = accumulated_text
            streamed = True
            now = time.monotonic()
            if now - last_draft_ts >= DRAFT_THROTTLE:
                await bot(SendMessageDraft(
                    chat_id=chat_id,
                    draft_id=draft_id,
                    text=accumulated_text,
                ))
                last_draft_ts = now

        # Clean up thinking message if stream yielded nothing
        if thinking_msg is not None:
            try:
                await thinking_msg.delete()
            except Exception:
                pass

        # Send final draft update + persistent message
        if streamed:
            await bot(SendMessageDraft(
                chat_id=chat_id,
                draft_id=draft_id,
                text=final_text,
            ))
        await message.answer(
            md_to_tg_html(final_text),
            parse_mode=ParseMode.HTML,
        )
    except Exception:
        logger.exception("Streaming failed for user %s, falling back", user.id)
        response = await session.handle_message(user.id, message.text)
        await message.answer(
            md_to_tg_html(response),
            parse_mode=ParseMode.HTML,
        )
