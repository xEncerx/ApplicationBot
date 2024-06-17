from aiogram import Dispatcher
from bot.middleware.throttling_middleware import ThrottlingMiddleware
from bot.middleware.ban_middleware import BanMiddleware

def setup_middleware(dp: Dispatcher) -> None:
	dp.message.middleware(ThrottlingMiddleware())
	dp.message.middleware(BanMiddleware())
	dp.callback_query.middleware(BanMiddleware())