from bot.data.application_model import ApplicationModel

from aiogram.types import FSInputFile, URLInputFile
from typing import Optional, BinaryIO, Union
from httpx import AsyncClient
import os

class FileUploader:
	"""
	Для загрузки используется файлообменник gofile.io
	Не доступен в РФ для просмотра файла используйте vpn|proxy
	Доступные сервера можно найти по ссылке:
	https://api.gofile.io/servers
	"""
	_SERVER = "store1"

	def __init__(self):
		self.session = AsyncClient()

	# Загрузка файлов на сервер и получение ссылки
	async def upload(self, file: BinaryIO) -> Optional[str]:
		_url = f"https://{self._SERVER}.gofile.io/contents/uploadfile"
		files = {"file": file}

		response = await self.session.post(_url, files=files)
		if response.status_code != 200: return

		_json = response.json()
		return _json["data"]["downloadPage"]


class ApplicationType:
	def __init__(self, application_data: dict, state: int):
		self.text = application_data.get("text")
		self.file_id = application_data.get("file_id")
		self.file_type = application_data.get("file_type")
		self.waiting_data = application_data.get("waiting_data")

		self.state = state

# Класс для хранения информации о заявке
class _ApplicationData:
	def __init__(self):
		self._data = {
			# user_id: question state
		}
		self._max_state = len(ApplicationModel.items())

	# Обновляем данные человека о заявке
	async def update(self, user_id: int, state: int = 1) -> None:
		if state <= self._max_state:
			self._data.update({user_id: state})

	# Удаляем человека
	async def delete(self, user_id: int) -> None:
		if self._data.get(user_id):
			del self._data[user_id]

	# Подгружаем данные о вопросе
	async def load(self, user_id: int) -> Optional[ApplicationType]:
		state = self._data.get(user_id)
		if not state:
			await self.update(user_id)

		if state-1 == self._max_state:
			return

		data = ApplicationModel.get(f"question_{state}")
		return ApplicationType(data, state)

	# Переход к следующему вопросу
	async def next(self, user_id: int) -> None:
		if not self._data.get(user_id):
			await self.update(user_id)

		self._data[user_id] += 1

	# На основе ответов создать текст заявки
	@staticmethod
	async def get_text_by_answers(data: dict) -> str:
		text = ""
		for key, value in data.items():
			if isinstance(value, tuple):
				value = "📥 <i>Файл был сохранен.</i>"
			question_text = ApplicationModel[key]["text"]
			text += f"<b>{question_text}:</b> <i>{value}</i>\n"

		return text


# Преобразование строки в нужный тип файла
def get_image(value: str) -> Union[FSInputFile, URLInputFile, str, None]:
	"""
	:param value: Путь к файлу / ссылка / file_id
	:return: FSInputFile / URLInputFile / file_id
	"""
	if os.path.exists(value):
		return FSInputFile(value)
	elif value.startswith("http"):
		return URLInputFile(value)
	elif value:
		return value
	return