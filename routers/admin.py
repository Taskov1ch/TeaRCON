from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from keyboards import kb_admin
from logger.group_logger import groups_logger
from logger.log import logger
from provider import db

rt = Router()

class States(StatesGroup):
	settings = State()
	commands = State()
	command_add = State()
	command_remove = State()
	roles_switch = State()
	give = State()
	remove = State()
	remove_user = State()
	remove_admin = State()
	add_user = State()
	add_admin = State()

async def settings_panel(message: Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	if await db.check_admin_user(chat_id):
		await message.reply(
			"Вы вошли в  Админ панель! Выберите действие",
			reply_markup = kb_admin.admin_panel_menu,
		)
		logger.info(f"Вход в  Админ панель выполнен пользователем с id: {chat_id}")
		await state.set_state(States.settings)

async def cancel_settings(message: Message, state: FSMContext) -> None:
	# выходит из  Админ панели
	await message.reply("Вы вышли из  Админ панели", reply_markup = kb_admin.main_menu)
	await state.clear()

async def back_to_state_settings(message: Message, state: FSMContext) -> None:
	# выходит из панели выбора действия над командами
	await message.reply("Возвращаемся назад!)", reply_markup = kb_admin.admin_panel_menu)
	await state.set_state(States.settings)

async def back_state_add(message: Message, state: FSMContext) -> None:
	# выходит из выдачи ролей
	await message.reply(
		"Возвращаемся назад!)", reply_markup = kb_admin.roles_switch_panel
	)
	await state.set_state(States.give)

async def back_state_remove(message: Message, state: FSMContext) -> None:
	# выходит из удаления роли
	await message.reply(
		"Возвращаемся назад!)", reply_markup = kb_admin.roles_switch_panel
	)
	await state.set_state(States.remove)

async def back_state_commands_switch(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Возвращаемся назад!", reply_markup = kb_admin.panel_commands_switch
	)
	await state.set_state(States.commands)

async def back_state_remove_roles_switcher(message: Message, state: FSMContext) -> None:
	# выходит из панели роли
	await message.reply("Возвращаемся назад!", reply_markup = kb_admin.admin_panel_menu)
	await state.set_state(States.settings)

async def back_state_roles(message: Message, state: FSMContext) -> None:
	# назад к панели ролей
	await message.reply("Возвращаемся назад!", reply_markup = kb_admin.roles_panel)
	await state.set_state(States.roles_switch)

async def back_state_remove_command(message: Message, state: FSMContext) -> None:
	# назад к панели действия над командами
	await message.reply(
		"Возвращаемся назад!)", reply_markup = kb_admin.panel_commands_switch
	)
	await state.set_state(States.commands)

async def roles_switch(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Выберите действие или вернитесь назад. ", reply_markup = kb_admin.roles_panel
	)
	await state.set_state(States.roles_switch)

async def give_roles(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Выберите какую роль нужно выдать", reply_markup = kb_admin.roles_switch_panel
	)
	await state.set_state(States.give)

async def remove_role(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Выберите какую роль нужно снять", reply_markup = kb_admin.roles_switch_panel
	)
	await state.set_state(States.remove)

async def remove_role_user(message: Message, state: FSMContext) -> None:
	await message.reply("Введите id для снятия прав", reply_markup = kb_admin.admin_back)
	await state.set_state(States.remove_user)

async def remove_role_admin(message: Message, state: FSMContext) -> None:
	await message.reply("Введите id для снятия роли", reply_markup = kb_admin.admin_back)
	await state.set_state(States.remove_admin)

async def roles_add_user(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Введите id для выдачи прав пользователя: ", reply_markup = kb_admin.admin_back
	)
	await state.set_state(States.add_user)

async def roles_add_admin(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Введите id для выдачи прав super- Админа: ", reply_markup = kb_admin.admin_back
	)
	await state.set_state(States.add_admin)

async def get_add_user_id(message: Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	if await db.user_exists(message.text):
		await message.reply(
			f'Пользователь с таким  id уже есть в списке.\nВведите другой id или нажмите "назад"'
		)
		await state.set_state(States.add_user)
	else:
		await groups_logger("Выдача роли обычного игрока: ", chat_id, message.text)
		await db.add_user(message.text)
		await message.reply(f"Роль 'обычная' выдана пользователю с id {message.text}")

async def get_add_admin_id(message: Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	if await db.check_admin_user(message.text):
		await message.reply(
			f'Этот id уже имеет роль  Администратора.\nВведите другой id или нажмите "назад"'
		)
		await state.set_state(States.add_admin)
	else:
		await groups_logger("Выдача роли  Администратора: ", chat_id, message.text)
		await db.add_admin(message.text)
		await message.reply(f"Вы выдали  Администратора пользователю с id {message.text}")

async def get_remove_user_id(message: Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	if not await db.user_exists(message.text):
		await message.reply(
			f'Пользователь с таким  id нет в списке.\nВведите другой id или нажмите "назад"'
		)
		await state.set_state(States.remove_user)
	else:
		await groups_logger("Снятие роли пользователя: ", chat_id, message.text)
		logger.info(f"{chat_id} - снял роль пользователя с {message.text}")
		await message.reply(await db.user_remove(message.text))

async def get_remove_admin_id(message: Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	if not await db.check_admin_user(message.text):
		await message.reply(
			f'В бд нет  Администратора с таким id.\nВведите другой id или нажмите "назад"'
		)
		await state.set_state(States.remove_admin)
	else:
		logger.info(f"{chat_id} - снял роль  Администратора с {message.text}")
		await groups_logger("Снятие роли  Администратора: ", chat_id, message.text)
		await message.reply(await db.admin_remove(message.text))

async def commands_settings(message: Message, state: FSMContext) -> None:
	await message.reply(
		f"Список заблокированных команд на данный момент:\n {await db.commands_all()}"
	)
	await message.reply(
		"Выберите, что нужно сделать. Добавить или удалить команды из списка. Либо вернитесь назад",
		reply_markup = kb_admin.panel_commands_switch,
	)
	await state.set_state(States.commands)

async def button_commands_add(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Пришлите команду или вернитесь назад", reply_markup = kb_admin.admin_back
	)
	await state.set_state(States.command_add)

async def button_commands_remove(message: Message, state: FSMContext) -> None:
	await message.reply(
		"Пришлите команду или вернитесь назад", reply_markup = kb_admin.admin_back
	)
	await state.set_state(States.command_remove)

async def command_add(message: Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	low = message.text.lower()
	if await db.command_exists(low):
		await message.reply(
			"Эта команда была заблокирована ранее. Введите другую или вернитесь назад"
		)
		logger.info(
			f"{chat_id} - попытался заблокировать команду {low}, но она уже в списках"
		)
		await groups_logger("Попытался заблокировать команду: ", chat_id, message.text)
		await state.set_state(States.command_add)

	else:
		await db.add_black_list(low)
		logger.info(f"{chat_id} - добавил команду в черный список. Команда: {low}")
		await groups_logger("Добавил команду в черный список", chat_id, message.text)
		await message.reply(
			"Команда была заблокирована.\nПришлите еще одну команду, или вернитесь назад"
		)
		await state.set_state(States.command_add)

async def command_remove(message: Message, state: FSMContext) -> None:
	chat_id = message.chat.id
	low = message.text.lower()
	if await db.command_exists(low):
		await db.remove_black_list(low)
		logger.info(f"{chat_id} - разблокировал команду {low}")
		await groups_logger("Удаление команды: ", chat_id, message.text)
		await message.reply(
			"Команда разблокирована!\nПришлите еще команду для разблокировки, или вернитесь назад"
		)
		await state.set_state(States.command_remove)
	else:
		logger.info(
			f"{chat_id} - попытался разблокировать команду {low}, но она не в списках"
		)
		await groups_logger(
			"Удаление команды (в списке отсутствует): ", chat_id, message.text
		)
		await message.reply(
			"Данная команда не находится в списке заблокированных.\nПришлите другую команду, или вернитесь назад"
		)
		await state.set_state(States.command_remove)

async def register_handlers() -> None:
	rt.message.register(settings_panel, F.text == "⚙ Управление", StateFilter(None))
	rt.message.register(cancel_settings, F.text == "◀ Отмена", States.settings)
	rt.message.register(back_to_state_settings, F.text == "⏹ Назад", States.commands)
	rt.message.register(back_state_add, F.text == "⏹ Назад", States.add_admin)
	rt.message.register(back_state_add, F.text == "⏹ Назад", States.add_user)
	rt.message.register(back_state_remove_roles_switcher, F.text == "⏹ Назад", States.roles_switch)
	rt.message.register(back_state_roles, F.text == "⏹ Назад", States.give)
	rt.message.register(back_state_roles, F.text == "⏹ Назад", States.remove)
	rt.message.register(back_state_remove, F.text == "⏹ Назад", States.remove_user)
	rt.message.register(back_state_remove, F.text == "⏹ Назад", States.remove_admin)
	rt.message.register(back_state_remove_command, F.text == "⏹ Назад", States.command_add)
	rt.message.register(back_state_remove_command, F.text == "⏹ Назад", States.command_remove)
	rt.message.register(roles_switch, F.text.startswith("📝 Роли"), States.settings)
	rt.message.register(give_roles, F.text == "📝 Выдать", States.roles_switch)
	rt.message.register(remove_role, F.text == "📝 Снять", States.roles_switch)
	rt.message.register(remove_role_user, F.text == "🪪 Обычный", States.remove)
	rt.message.register(remove_role_admin, F.text == "🪪 Админ", States.remove)
	rt.message.register(get_remove_user_id, States.remove_user)
	rt.message.register(get_remove_admin_id, States.remove_admin)
	rt.message.register(roles_add_user, F.text == "🪪 Обычный", States.give)
	rt.message.register(roles_add_admin, F.text == "🪪 Админ", States.give)
	rt.message.register(get_add_user_id, States.add_user)
	rt.message.register(get_add_admin_id, States.add_admin)
	rt.message.register(commands_settings, F.text == "📝 Команды", States.settings)
	rt.message.register(button_commands_add, F.text == "⛔ Добавить", States.commands)
	rt.message.register(button_commands_remove, F.text == "🗑 Удалить", States.commands)
	rt.message.register(command_add, States.command_add)
	rt.message.register(command_remove, States.command_remove)