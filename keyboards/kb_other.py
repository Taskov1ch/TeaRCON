from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(resize_keyboard = True, keyboard = [
	[
		KeyboardButton(text = "🆔 Айди"),
		KeyboardButton(text = "🆘 Инфо")
	],
	[
		KeyboardButton(text = "🆘 Поддержка")
	]
])