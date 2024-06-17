from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопка назад
def back_button(value: str) -> InlineKeyboardMarkup:
	button = [
		[
			InlineKeyboardButton(text="🔙 Назад", callback_data=f"back|{value}")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=button)

# Клавиатура создания заявки
def create_application() -> InlineKeyboardMarkup:
	button = [
		[
			InlineKeyboardButton(text="➕ Создать заявку", callback_data="create_application")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=button)

# Клавиатура подтверждения заявки
def confirm_application() -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_application")
		],
		[
			InlineKeyboardButton(text="🗑 Заполнить заново", callback_data="recreate_application")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=buttons)

# Клавиатура администратора
def admin_application(user_id: int) -> InlineKeyboardMarkup:
	buttons = [
		[
			InlineKeyboardButton(text="➕ Одобрить", callback_data=f"#accept|{user_id}")
		],
		[
			InlineKeyboardButton(text="➖ Отклонить", callback_data=f"#reject|{user_id}"),
			InlineKeyboardButton(text="💤 Игнорировать", callback_data=f"#ignore|{user_id}")
		],
		[
			InlineKeyboardButton(text="🤬 Забанить", callback_data=f"#ban|{user_id}")
		]
	]
	return InlineKeyboardMarkup(inline_keyboard=buttons)