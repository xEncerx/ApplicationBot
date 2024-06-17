from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types, Router

from bot.data.config import TEXT, welcomeImage
from bot.utils.message import text_editor
from bot.utils import application
import bot.markups as nav

router = Router()

@router.message(Command("start"), StateFilter("*"))
async def start(message: types.Message, state: FSMContext):
	# Удаляем заявку, если есть
	await application.delete(message.from_user.id)
	await state.clear()

	await text_editor(
		TEXT.welcome.format(name=message.from_user.first_name),
		event=message,
		reply_markup=nav.create_application(),
		photo=welcomeImage
	)