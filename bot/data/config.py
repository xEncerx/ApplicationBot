from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from bot.utils.const_functions import get_image
from bot.data.bot_text import BotText
from bot.database.api import DBApi

import logging as logger
import configparser
import os

__version__ = "0.1"
# -----------------------------PROJECT PATH-----------------------------
PATH = os.getcwd()

DB_PATH = os.path.join(PATH, "bot", "database", "data.db")
SETTINGS_PATH = os.path.join(PATH, "config.ini")
# -------------------------------SETTINGS-------------------------------
botConfig = configparser.ConfigParser()
botConfig.read(SETTINGS_PATH)
chatConfig = botConfig["CHAT"]
botConfig = botConfig["SETTINGS"]

TOKEN = botConfig["token"]
welcomeImage = get_image(botConfig["welcomeImage"])
adminID = botConfig["adminID"].strip().split(",")
adminID = list(map(int, adminID))
adminChat = botConfig["adminChat"]
allowReapplication = botConfig.getboolean("allowReapplication")
reapplicationLevel = [i.strip() for i in botConfig["reapplicationLevel"].split(",")]

chatID = chatConfig["chatID"]
generateLink = chatConfig.getboolean("generateLink")
expireDelta = float(chatConfig["expireDelta"])
memberLimit = int(chatConfig["memberLimit"])
staticLink = chatConfig["staticLink"]
# -------------------------------AIOGRAM--------------------------------
bot = Bot(
	token=TOKEN,
	default=DefaultBotProperties(
		parse_mode="HTML"
	)
)
dp = Dispatcher(storage=MemoryStorage())
# -------------------------------LOGGING--------------------------------
logger.getLogger("httpx").setLevel(logger.WARNING)
logger.basicConfig(level=logger.INFO)
# -------------------------------FUNCTION-------------------------------
db = DBApi(DB_PATH)
TEXT = BotText()