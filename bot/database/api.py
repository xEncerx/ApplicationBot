from typing import Any
import aiosqlite

class ClientStatus:
	EMPTY = "EMPTY"
	PENDING = "PENDING"
	ACCEPTED = "ACCEPTED"
	REJECTED = "REJECTED"
	BANNED = "BANNED"


class DBApi:
	def __init__(self, db_path: str):
		self._db_path = db_path
		self.client = Client(self)

	# Ф-ция запроса
	async def db_request(
			self,
			query: str,
			param: tuple = (),
			fetchone: bool = False,
			fetchall: bool = False
	) -> Any:
		async with aiosqlite.connect(self._db_path) as connection:
			async with connection.execute(query, param) as cursor:
				await connection.commit()
				if fetchone:
					return await cursor.fetchone()
				elif fetchall:
					return await cursor.fetchall()

	# Создание БД
	async def create_db(self) -> None:
		await self.db_request(
			"""
			CREATE TABLE IF NOT EXISTS "client" (
			"user_id"	INTEGER NOT NULL,
			"status"	TEXT NOT NULL,
			PRIMARY KEY("user_id")
			)
			"""
		)


class Client:
	def __init__(self, parent: DBApi):
		self._parent = parent

	# Добавление пользователя
	async def add(self, user_id: int) -> None:
		await self._parent.db_request(
			"INSERT INTO client VALUES (?, ?)",
			(user_id, ClientStatus.EMPTY,)
		)

	# Получение информации о пользователе
	async def get(self, user_id: int, data: str) -> str:
		result = await self._parent.db_request(
			f"SELECT {data} FROM client WHERE user_id = ?",
			(user_id,), fetchone=True
		)
		return result[0]

	# Обновление информации о пользователе
	async def update(self, user_id: int, **kwargs) -> None:
		if not kwargs: return

		data = ", ".join([f"{row}='{value}'" for row, value in kwargs.items()])
		await self._parent.db_request(
			f"UPDATE client SET {data} WHERE user_id = ?",
			(user_id,)
		)

	# Проверка на существование пользователя
	async def exists(self, user_id: int) -> bool:
		result = await self._parent.db_request(
			"SELECT 1 FROM client WHERE user_id = ?",
			(user_id,), fetchone=True
		)
		return bool(result)

