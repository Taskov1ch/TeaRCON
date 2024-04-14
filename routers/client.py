from aiogram import Dispatcher, types
from aiogram.filters import StateFilter
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import kb_admin, kb_client
from logger.group_logger import groups_logger
from logger.log import logger
from minecraft import rcon
from provider import db
from aiogram import Router, F

rt = Router()

class States(StatesGroup):
	rcon = State()

async def rcon_cmd(message: types.Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	user_id = message.from_user.id
	if await db.check_admin_user(chat_id) or await db.user_exists(chat_id):
		logger.info(f"Пользователь с id {user_id} вошел в rcon консоль с правами администратора")
		await message.reply(
			"Теперь пришли команду",
			reply_markup = kb_client.rcon_cancel
		)
		await state.set_state(States.rcon)
	else:
		await message.reply("У вас нет доступа к данной команде.")

async def cancel_state_rcon(message: types.Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	if await db.check_admin_user(chat_id):
		await message.reply(
			"Ты вышел из консоли. Прикажи что исполнять!",
			reply_markup = kb_admin.main_menu,
		)
	else:
		await message.reply(
			"Ты вышел из консоли. Каковы будут дальнейшие действия?",
			reply_markup = kb_client.main_menu,
		)
	await state.clear()

async def get_command(message: types.Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	low = message.text.lower()
	command = low.split(" ", 1)
	user_id = message.from_user.id
	if not await db.check_admin_user(chat_id):
		if await db.command_exists(command[0]):
			logger.info(f"Пользователь с id {user_id} попытался выполнить заблокированную команду")
			await groups_logger("RCON: ", user_id, message.text)
			await message.reply("Команда заблокирована! Используйте другую :)")
		else:
			logger.info(f"Пользователь с id {user_id} выполнил команду: {message.text}")
			await groups_logger("RCON: ", user_id, message.text)
			response = rcon.command_execute(low)
			await message.reply(f"Команда выполнена. Ответ сервера: {response}")
			# await message.answer("Вы можете продолжить выполнять команды. Просто пришлите мне их. Или введите отмена")
	else:
		response = rcon.command_execute(low)
		await message.reply(f"Команда выполнена. Ответ сервера: {response}")
		logger.info(f"Администратор с id {user_id} выполнил команду: {message.text}")

async def register_handlers() -> None:
	rt.message.register(rcon_cmd, F.text == "❗ Ркон", StateFilter(None))
	rt.message.register(rcon_cmd, Command("rcon"), StateFilter(None))
	rt.message.register(cancel_state_rcon, F.text == "◀ Отмена", States.rcon)
	rt.message.register(get_command, States.rcon)