from aiogram.types import URLInputFile, FSInputFile, InlineKeyboardMarkup, Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from bot.data.config import bot
from typing import Union

# Удаление сообщения
async def delete_message(chat_id: int, message_id: int) -> None:
	try:
		await bot.delete_message(chat_id=chat_id, message_id=message_id)
	except TelegramBadRequest:
		pass

# Отправка сообщения с обработкой ошибки
async def send_message(chat_id: int, text: str, reply_markup: InlineKeyboardMarkup = None) -> Message:
	try:
		msg = await bot.send_message(
			chat_id,
			text,
			reply_markup=reply_markup,
			disable_web_page_preview=True
		)
	except TelegramBadRequest:
		msg = None

	return msg


# Умная отправка сообщений
async def text_editor(
		text: str,
		event: Union[Message, CallbackQuery],
		photo: Union[URLInputFile, FSInputFile, str] = None,
		document: Union[URLInputFile, FSInputFile, str] = None,
		reply_markup: InlineKeyboardMarkup = None,
		**kwargs
) -> Message:
	chat_id = event.from_user.id

	if isinstance(event, Message):
		message_id = event.message_id
	elif isinstance(event, CallbackQuery):
		message_id = event.message.message_id
	else:
		raise ValueError("The event should be a Message or CallbackQuery types")

	if photo or document:
		# Удаляем текущее сообщение
		await delete_message(chat_id, message_id)

		try:
			if photo:
				msg = await bot.send_photo(chat_id, photo, caption=text, reply_markup=reply_markup)
			elif document:
				msg = await bot.send_document(chat_id, document, caption=text, reply_markup=reply_markup)
		except TelegramBadRequest:
			# Если не удается отправить фото/файл, то отправляем сообщение
			msg = await send_message(chat_id, text, reply_markup=reply_markup)
	else:
		try:
			# Редактируем текст текущего сообщения
			msg = await bot.edit_message_text(text, chat_id, message_id, reply_markup=reply_markup)
		except TelegramBadRequest:
			# Если не удается, то удаляем его и отправляем новое
			await delete_message(chat_id, message_id)
			msg = await send_message(chat_id, text, reply_markup=reply_markup)

	return msg
