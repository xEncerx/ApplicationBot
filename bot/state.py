from aiogram.fsm.state import StatesGroup, State

# State для Клиента
class Client(StatesGroup):
	class Answers(StatesGroup):
		data = State()

# State для Админа
class Admin(StatesGroup):
	class FileId(StatesGroup):
		get_id = State()
