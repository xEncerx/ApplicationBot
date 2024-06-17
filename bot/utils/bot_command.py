from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from aiogram import Bot

from bot.data.config import adminID

# Команды для юзеров
user_commands = [
    BotCommand(command="start", description="♻️ Restart bot")
]

# Команды для админов
admin_commands = [
    BotCommand(command="start", description="♻️ Restart bot"),
    BotCommand(command="admin", description="🌀 Admin Menu"),
    BotCommand(command="db_backup", description="📦 DataBase Backup"),
    BotCommand(command="file_id", description="📂 Get FileID")
]

# Установка команд
async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())

    for admin in adminID:
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
        except:
            pass