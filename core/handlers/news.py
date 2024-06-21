from aiogram import Router, Bot, F
from aiogram.types import Message

from config import settings
from core.handlers.form import user_data

news_router = Router()


@news_router.message(F.text.startswith("/send_news"))
async def send_news(message: Message, bot: Bot):
    if message.from_user.id == settings.admin_id:  # Проверка, что команду отправил админ
        try:
            news = message.text.split('/send_news ', 1)[1]
            print(news)
            print(user_data)
            for user_id in user_data.keys():
                print(user_id)
                await bot.send_message(chat_id=user_id, text=news)
        except IndexError:
            await message.reply("Пожалуйста, добавьте текст новости после команды.")
    else:
        await message.reply("У вас нет прав для выполнения этой команды.")