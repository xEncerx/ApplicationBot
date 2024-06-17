from aiogram.types import FSInputFile, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types, Router

from bot.data.config import TEXT, DB_PATH, bot, db
from bot.filters import IsAdmin, AnyContentType
from bot.utils.message import text_editor
from bot.state import Admin
import bot.markups as nav

from datetime import datetime
import os

router = Router()

# Резервная копия Базы Данных
@router.message(Command("db_backup"), IsAdmin())
async def db_backup(message: types.Message, state: FSMContext):
	await state.clear()

	time = datetime.now().strftime('%H:%M %d.%m.%Y')

	if not os.path.exists(DB_PATH):
		await message.reply("❗️ Не удалось найти Базу Данных, создаю...")
		await db.create_db()
		await message.reply("✅ База Данных была создана")
		return

	await bot.send_document(
		message.from_user.id,
		document=FSInputFile(DB_PATH),
		caption=f"<b>📦 #BACKUP | <code>{time}</code></b>"
	)

# Получение file_id
@router.message(Command("file_id"), IsAdmin())
async def get_file_id(message: types.Message, state: FSMContext):
	await state.clear()

	await text_editor(
		TEXT.admin.send_file,
		event=message,
		reply_markup=nav.back_button("main_menu")
	)
	await state.set_state(Admin.FileId.get_id)

# Отправка file_id
@router.message(
	StateFilter(Admin.FileId.get_id),
	IsAdmin(),
	AnyContentType(ContentType.PHOTO, ContentType.DOCUMENT)
)
async def return_file_id(message: types.Message, state: FSMContext):
	match message.content_type:
		case ContentType.PHOTO:
			file_id = message.photo[-1].file_id
		case ContentType.DOCUMENT:
			file_id = message.document.file_id
		case _:
			file_id = "UNKNOWN"

	await message.reply(f"<b>📁 #FILE_ID\n<code>{file_id}</code></b>")
	await state.clear()