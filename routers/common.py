from aiogram import Dispatcher, Router
from aiogram.filters.command import Command
from aiogram.types import Message
from keyboards import kb_admin, kb_client, kb_other
from provider import db

rt = Router()

async def start(message: Message):
	chat_id = message.chat.id
	if await db.check_admin_user(chat_id):
		await message.reply(
			"Привет друг! О, ты же админ! Так начни управлять.",
			reply_markup = kb_admin.main_menu,
		)
	elif await db.user_exists(chat_id):
		await message.reply(
			"Привет друг. У тебя есть доступ к консоли, удачи!",
			reply_markup = kb_client.main_menu,
		)
	else:
		await message.reply(
			"Привет друг! Введи /info для отображения информации о боте!",
			reply_markup = kb_other.main_menu,
		)

async def register_handlers() -> None:
	rt.message.register(start, Command("start"))