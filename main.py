from bot.data.config import dp, db, bot, logger, __version__
from bot.utils.bot_command import set_commands
from bot.middleware import setup_middleware
from bot.handlers import routers

import asyncio

# Запуск бота
async def main():
	# Создание БазыДанных при необходимости
	# await db.create_db()

	dp.include_routers(*routers)

	await set_commands(bot)
	setup_middleware(dp)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)

if __name__ == "__main__":
	print("-_-_- Bot made by @Encer -_-_-",
		  f"-_-_-_- Version: {__version__} -_-_-_-",
		  "-_-_- Thanks for using -_-_-",
		  sep="\n")
	try:
		# Исправление "RuntimeError: Event loop is closed" для Windows
		# if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win"):
		#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

		asyncio.run(main())
	except (KeyboardInterrupt, SystemExit):
		logger.warning("-_-_- Bot was stopped -_-_-")
