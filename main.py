import asyncio
from aiogram import Bot, Dispatcher
from bot import register_handlers
from config import TELEGRAM_TOKEN
from deal_fetcher import fetch_and_post_deals
from utils import setup_logger

logger = setup_logger("main")

async def main():
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    register_handlers(dp)

    logger.info("🤖 Bot has started successfully and is now running...")

    # Start background task to post deals every few minutes
    asyncio.create_task(fetch_and_post_deals(bot))

    # Start polling to handle commands and messages
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot has stopped!")
