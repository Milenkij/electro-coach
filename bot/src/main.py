import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher

from .bot import router
from .config import config
from . import db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

MIGRATION_PATH = str(Path(__file__).resolve().parent.parent / "migrations" / "001_init.sql")


async def main() -> None:
    logger.info("Starting ElectroCoach bot...")

    # Init database
    await db.init_pool(config.database_url)
    await db.run_migration(MIGRATION_PATH)
    logger.info("Database ready")

    # Init bot
    bot = Bot(token=config.telegram_token)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("Bot is polling...")
    try:
        await dp.start_polling(bot)
    finally:
        await db.close_pool()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
