from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(resize_keyboard = True, keyboard = [
	[
		KeyboardButton(text = "🆔 Айди"),
		KeyboardButton(text = "❗ Ркон")
	],
	[
		KeyboardButton(text = "🆘 Инфо"),
		KeyboardButton(text = "⚙ Управление")
	],
	[
		KeyboardButton(text = "🆘 Поддержка")
	]
])

rcon_cancel = ReplyKeyboardMarkup(resize_keyboard = True, keyboard = [
	[
		KeyboardButton(text = "◀ Отмена")
	]
])