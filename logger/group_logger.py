from aiogram import Bot
from dotenv import load_dotenv
from provider import db
from resources import config
import os

load_dotenv()

bot = Bot(token = os.getenv("TOKEN"))

async def groups_logger(prefix: str, user_id: str, message: str) -> None:
	if not config.telegram()["on_logger_group"]:
		return
	try:
		if await db.check_admin_user(user_id):
			message = f"{prefix} Админ с ID {user_id} - ввел команду: {message}"
			await bot.send_message(config.telegram()["logger_chat_id"], message)
		else:
			message = f"{prefix} Пользователь с ID {user_id} - ввел команду: {message}"
			await bot.send_message(config.telegram()["logger_chat_id"], message)
	except Exception as e:
		pass