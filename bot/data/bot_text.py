# Текст меняем под свои нужны
# _____________
# Если в исходном тексте есть переменные в фигурных скобках,
# их можно перемещать или не использовать совсем

class BotText:
	welcome = "👋 Добро пожаловать <b>{name}</b>\n\n" \
			  "🪬 Сейчас осуществляется прием заявок в Our Team \n\n" \
			  "📬 Успей подать заявку, и присоединиться к нашей команде"

	client_answers = "Ответы на наши вопросы:\n" \
					 "{answers}"

	class error:
		no_data = "❗ <b> ️Необходимо корректно заполнить данные вопроса</b>"
		incorrect_format = "⚠️ <b>На этот вопрос нужно ответить по-другому</b>"
		banned = "❗️ К сожалению ваш аккаунт был заблокирован администратором"
		file_too_big = "❗️ Файл не был сохранен. Его размер должен быть меньше 20 мбайт."

	class admin:
		client_answers = "Поступила новая заявка от (<code>{user_id}</code>)[@{username}]\n" \
						 "Ответы на вопросы:\n\n" \
						 "{answers}"
		send_file = "📥 <b>Пришлите мне файл, чтобы получить его file_id</b>"

	class application:
		sent = "🚀 <b>Заявка отправлена, ожидайте</b>"
		rejected = "Извините, вы нам не подходите"
		processed_accepted = "✅ Заявка одобрена!"
		processed_rejected = "❌ Заявка отклонена!"
		processed_ban = "👍 Пользователь послан нах*й"
		processed_ignored = "💤 Заявка проигнорирована!"
		cant_be_created = "К сожалению вы не можете подать заявку снова"
		on_consideration = "Ваша заявка находиться на рассмотрение"

		accepted = "Поздравляю, вы приняты в нашу команду \n\n" \
				   "Ссылка для вступления в чат: {link} \n\n" \
				   "<b>ЧИТАЙТЕ ВСЕ МАНУАЛЫ В ЗАКРЕПЕ </b>"