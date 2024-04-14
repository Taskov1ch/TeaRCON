from aiogram import Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters.command import Command

rt = Router()

async def id_cmd(message: Message) -> None:
	chat_id = message.chat.id
	await message.reply(f"Ваш id: {chat_id}")

async def info_cmd(message: Message) -> None:
	await message.reply("Бот написан на полностью бесплатной основе\nРазработчик: teanus.ru")

async def support_cmd(message: Message) -> None:
	await message.reply("Сайт: teanus.ru")

async def register_handlers() -> None:
	rt.message.register(id_cmd, Command("id"))
	rt.message.register(info_cmd, Command("info"))
	rt.message.register(support_cmd, Command("support"))
	rt.message.register(id_cmd, F.text == "🆔 Айди")
	rt.message.register(info_cmd, F.text == "🆘 Инфо")
	rt.message.register(support_cmd, F.text == "🆘 Поддержка")