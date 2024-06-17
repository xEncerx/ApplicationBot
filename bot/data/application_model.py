class ApplicationType:
	TEXT: str = "text"
	PHOTO: str = "photo"
	DOCUMENT: str = "document"
	NONE = "unknown"


# Инструкция по созданию модели заявок:
# https://telegra.ph/Redaktirovanie-modeli-zayavok-06-11
ApplicationModel = {
	# Отправляем текстовое сообщение, ожидаем текст
	"question_1": {
		"text": "Как тебя зовут?",
		"file_id": None,
		"file_type": ApplicationType.NONE,
		"waiting_data": ApplicationType.TEXT
	},
	# Отправляем фотографию с описанием, ожидаем текст
	"question_2": {
		"text": "Что изображено на фотографии?",
		"file_id": "AgACAgIAAxkBAAIft2Zp4CGGP-wErLOxrby09OIw6YdlAAK64jEbNB9RS9ac39NJshsQAQADAgADeAADNQQ",
		"file_type": ApplicationType.PHOTO,
		"waiting_data": ApplicationType.TEXT
	},
	# Отправляем файл с описанием, ожидаем фотографию(возможно с описанием)
	"question_3": {
		"text": "Пришли понравившуюся фотографию из файла:",
		"file_id": "BQACAgIAAxkBAAIe9mZnDDf40_hVzO0LmJ-TDk9MT6NxAALPTwACvkY4S219J8nol8z9NQQ",
		"file_type": ApplicationType.DOCUMENT,
		"waiting_data": ApplicationType.PHOTO
	},
	# Отправляем текстовое сообщение, ожидаем документ(возможно с описанием)
	"question_4": {
		"text": "Пришли файл",
		"file_id": None,
		"file_type": ApplicationType.NONE,
		"waiting_data": ApplicationType.DOCUMENT
	}
}