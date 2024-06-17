from bot.filters import StartsWith, IsAdmin
from bot.database.api import ClientStatus
from bot.data.config import *

from datetime import datetime, timedelta
from aiogram import types, Router

router = Router()

# Админ принимает заявку
@router.callback_query(StartsWith("#accept"), IsAdmin())
async def accept(call: types.CallbackQuery):
	user_id = call.data.split("|")[1]

	if generateLink:
		if expireDelta == -1: expire_date = None
		else: expire_date = datetime.now() + timedelta(minutes=expireDelta)

		if memberLimit == -1: member_limit = None
		else: member_limit = memberLimit

		# Создаем ссылку на вступление
		link = await bot.create_chat_invite_link(
			chat_id=chatID,
			expire_date=expire_date,
			member_limit=member_limit
		)
		link = link.invite_link
	else:
		link = staticLink

	await bot.send_message(
		user_id,
		TEXT.application.accepted.format(link=link),
		disable_web_page_preview=True
	)
	# Меняем статус клиента на ACCEPTED
	await db.client.update(user_id, status=ClientStatus.ACCEPTED)

	await call.message.edit_text(TEXT.application.processed_accepted)

# Админ отклонил заявку
@router.callback_query(StartsWith("#reject"), IsAdmin())
async def reject(call: types.CallbackQuery):
	user_id = call.data.split("|")[1]

	await bot.send_message(
		user_id,
		TEXT.application.rejected
	)
	# Меняем статус клиента на REJECTED
	await db.client.update(user_id, status=ClientStatus.REJECTED)

	await call.message.edit_text(TEXT.application.processed_rejected)

# Админ игнорирует заявку
@router.callback_query(StartsWith("#ignore"), IsAdmin())
async def ignore(call: types.CallbackQuery):
	await call.message.edit_text(TEXT.application.processed_ignored)

# Админ банит пользователя
@router.callback_query(StartsWith("#ban"), IsAdmin())
async def ban(call: types.CallbackQuery):
	user_id = call.data.split("|")[1]

	# Меняем статус клиента на BANNED
	await db.client.update(user_id, status=ClientStatus.BANNED)

	await call.message.edit_text(TEXT.application.processed_ban)