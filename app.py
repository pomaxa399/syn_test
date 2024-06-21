import asyncio
import logging
import sys
from config import settings

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart

from core.handlers.basic import get_start
from core.handlers.form import form_router
from core.handlers.news import news_router
from core.utils.commands import set_command

TOKEN = settings.bot_token


dp = Dispatcher()
dp.message.register(get_start,CommandStart())
dp.include_router(form_router)
dp.include_router(news_router)


@dp.startup()
async def on_startup(bot: Bot):
    await set_command(bot)
    await bot.send_message(settings.admin_id, text='Бот запущен!')



@dp.shutdown()
async def on_shutdown(bot: Bot):
    await bot.send_message(settings.admin_id, text='Бот остановлен!')


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    try:
        # And the run events dispatching
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
