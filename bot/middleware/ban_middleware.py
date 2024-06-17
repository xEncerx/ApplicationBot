from typing import Callable, Dict, Awaitable, Any, Union
from aiogram.types import Update, Message, CallbackQuery

from aiogram import BaseMiddleware
from bot.database.api import ClientStatus
from bot.data.config import db, TEXT

class BanMiddleware(BaseMiddleware):
	async def __call__(
			self,
			handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
			event: Union[Message, CallbackQuery],
			data: Dict[str, Any],
	) -> Any:
		if not await db.client.exists(event.from_user.id):
			await db.client.add(event.from_user.id)
			return await handler(event, data)

		user_status = await db.client.get(event.from_user.id, "status")
		if user_status != ClientStatus.BANNED:
			return await handler(event, data)

		if isinstance(event, Message):
			await event.answer(TEXT.error.banned)
		elif isinstance(event, CallbackQuery):
			await event.answer(TEXT.error.banned, show_alert=True)
