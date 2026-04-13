import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ChatAction, ChatMemberStatus, ParseMode
from aiogram.filters import Command

from . import session
from .formatting import md_to_tg_html

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
    if user is None or not message.text:
        return

    # Restore state if needed (bot might have restarted)
    if session.get_state(user.id) == session.UserState.IDLE:
        await session.restore_state(user.id)

    # Show typing indicator
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    response = await session.handle_message(user.id, message.text)
    await message.answer(md_to_tg_html(response), parse_mode=ParseMode.HTML)
