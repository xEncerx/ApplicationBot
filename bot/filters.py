from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter

from bot.data.config import adminID

from typing import Union

# Фильтр - данные начинаются с ...
class StartsWith(BaseFilter):
	def __init__(self, text: str):
		self.text = text

	async def __call__(self, event: Union[Message, CallbackQuery]):
		if isinstance(event, Message):
			return event.text.startswith(self.text)
		elif isinstance(event, CallbackQuery):
			return event.data.startswith(self.text)

# Фильтр - одно из условий
class AnyData(BaseFilter):
	def __init__(self, *args):
		self.data = set(args)

	async def __call__(self, call: CallbackQuery):
		return call.data in self.data

# Фильтр на админа
class IsAdmin(BaseFilter):
	async def __call__(self, event: Union[Message, CallbackQuery]):
		return event.from_user.id in adminID

# Фильтр контента
class AnyContentType(BaseFilter):
	def __init__(self, *args):
		self.types = args

	async def __call__(self, event: Union[Message, CallbackQuery]):
		return event.content_type in self.types