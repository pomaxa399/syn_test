from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_command(bot: Bot) -> None:
    commands = [
        BotCommand(
            command='start',
            description='Начало работы'
        ),
        BotCommand(
            command='send_news',
            description='Отправить новость'
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
