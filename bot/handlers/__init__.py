from .admin import admin_commands, application_action
from .client import start, application
from bot.handlers import back_button

from aiogram import Router

routers: list[Router] = [
	start.router,
	application.router,
	application_action.router,
	admin_commands.router,
	back_button.router
]