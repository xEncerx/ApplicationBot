from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.types import ContentType
from aiogram import types, Router, F

from bot.data.application_model import ApplicationModel
from bot.filters import AnyContentType, AnyData
from bot.utils import application, file_uploader
from bot.database.api import ClientStatus
from bot.utils.message import text_editor
from bot.data.config import *
from bot.state import Client
import bot.markups as nav

from typing import Union
from uuid import uuid4
import asyncio

router = Router()

# Создание заявки
@router.callback_query(StateFilter("*"), F.data == "create_application")
async def create_application(call: types.CallbackQuery, state: FSMContext) -> None:
	# Текущий статус клиента
	client_status = await db.client.get(call.from_user.id, "status")

	# Проверка на возможность создания заявки
	if not allowReapplication or client_status not in reapplicationLevel:
		await call.answer(TEXT.application.cant_be_created, show_alert=True)
		return

	# Создаем заявку
	await application.update(call.from_user.id)
	# Отправляем 1-ый вопрос
	await send_question(call, state)
	await state.set_state(Client.Answers.data)

# Отправляем пользователю вопрос
async def send_question(event: Union[types.Message, types.CallbackQuery], state: FSMContext) -> None:
	# Загружаем информацию вопроса из модели
	application_data = await application.load(event.from_user.id)

	# Если дошли до конца всех вопросов
	if not application_data:
		# Получаем ответы
		data = (await state.get_data()).get("answers")
		# Формируем текст по ответам и отправляем
		await bot.send_message(
			event.from_user.id,
			await application.get_text_by_answers(data),
			reply_markup=nav.confirm_application()
		)
		return

	send_data = {
		application_data.file_type: application_data.file_id
	}
	await text_editor(
		application_data.text,
		event=event,
		reply_markup=nav.back_button("main_menu"),
		**send_data
	)

# Получение ответа на вопрос
@router.message(
	StateFilter(Client.Answers.data),
	AnyContentType(ContentType.TEXT, ContentType.PHOTO, ContentType.DOCUMENT)
)
async def answer_question(message: types.Message, state: FSMContext) -> None:
	# Загружаем информацию вопроса из модели
	application_data = await application.load(message.from_user.id)
	message_type = message.content_type

	# Проверяем на соответствие типа сообщение с указанным в настройках
	if message_type != application_data.waiting_data:
		await message.answer(TEXT.error.incorrect_format)
		return

	# Сопоставляем тип сообщение с указанным в настройках
	match message_type:
		case ContentType.TEXT:
			input_data = message.text

		case ContentType.PHOTO:
			caption = message.caption
			photo = message.photo[-1]
			input_data = (caption, photo.file_id, f"{uuid4()}.png")

		case ContentType.DOCUMENT:
			caption = message.caption
			document = message.document
			size = document.file_size

			# У тг есть ограничение на скачивание файла более 20 мбайт
			if size // 1024 > 20_000:
				await message.reply(TEXT.error.file_too_big)
				return

			input_data = (caption, document.file_id, f"{uuid4()}.{document.file_name.split('.')[1]}")
		case _:
			return

	# Обновляем данные ответов
	client_answer = (await state.get_data()).get("answers", {})
	client_answer.update(
		{f"question_{application_data.state}": input_data}
	)
	await state.update_data(answers=client_answer)

	# Переход к следующему вопросу
	await application.next(message.from_user.id)
	await send_question(message, state)

# Обработка кнопок подтверждения / заполнить заново
@router.callback_query(
	StateFilter(Client.Answers.data),
	AnyData("confirm_application", "recreate_application")
)
async def confirmation(call: types.CallbackQuery, state: FSMContext) -> None:
	action = call.data

	# Подтверждение заявки
	if action == "confirm_application":
		client_answers = (await state.get_data()).get("answers")
		# Отправляем ответы пользователя админу
		asyncio.create_task(
			copy_to_admin(call, client_answers, call.from_user.id)
		)
		await text_editor(
			TEXT.application.sent,
			event=call
		)
		# Обновляем статус заявки на PENDING
		await db.client.update(call.from_user.id, status=ClientStatus.PENDING)

		# Удаляем заявку
		await application.delete(call.from_user.id)

	# Заполнить заново
	elif action == "recreate_application":
		# Удаляем заявку
		await application.delete(call.from_user.id)
		await text_editor(
			TEXT.welcome,
			event=call,
			reply_markup=nav.create_application()
		)

	await state.clear()

# Отправить заявку в админ чат
async def copy_to_admin(
		call: types.CallbackQuery,
		client_data: dict,
		client_id: int
):
	answers = ""
	for key, value in client_data.items():
		# Если пользователем был загружен файл,
		# грузим его на сервер и получаем ссылку
		if isinstance(value, tuple):
			caption, file_id, file_name = value
			file_obj = await bot.download(file_id)

			# Загрузка файла на сервер
			url = await file_uploader.upload(file_obj)

			value = f"[{caption}](<a href='{url}'>Просмотреть файл</a>)"

		question_text = ApplicationModel[key]["text"]
		answers += f"<b>{question_text}</b>: <i>{value}</i>\n"

	# Отправляем заявку админу
	await bot.send_message(
		chat_id=adminChat,
		text=TEXT.admin.client_answers.format(user_id=call.from_user.id,
											  username=call.from_user.username,
											  answers=answers),
		reply_markup=nav.admin_application(client_id),
		disable_web_page_preview=True
	)
