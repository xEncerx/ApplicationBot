from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram import types, Router

from bot.utils import application
from bot.data.config import TEXT
from bot.filters import StartsWith
from bot.utils.message import text_editor
import bot.markups as nav

router = Router()

# обработка кнопки "Назад"
@router.callback_query(StateFilter("*"), StartsWith("back|"))
async def back_handler(call: types.CallbackQuery, state: FSMContext):
	action = call.data.split("|")[1]
	await state.clear()

	if action == "main_menu":
		# Удаление пользовательской заявки
		await application.delete(call.from_user.id)

		await text_editor(
			TEXT.welcome.format(name=call.from_user.first_name),
			event=call,
			reply_markup=nav.create_application()
		)

