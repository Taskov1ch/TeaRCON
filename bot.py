from add_super_admin import console_add_super_admin
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from logger.log import logger
from routers import other, common, client, admin
import asyncio
import os

load_dotenv()

bot = Bot(token = os.getenv("TOKEN"))
dp = Dispatcher()

async def on_startup(bot: Bot) -> None:
	logger.info("Бот запущен!")
	await console_add_super_admin()

async def run() -> None:
	dp.startup.register(on_startup)
	dp.include_routers(other.rt)
	await other.register_handlers()
	dp.include_routers(common.rt)
	await common.register_handlers()
	dp.include_routers(client.rt)
	await client.register_handlers()
	dp.include_routers(admin.rt)
	await admin.register_handlers()

	await bot.delete_webhook(drop_pending_updates = True)
	await dp.start_polling(bot)

if __name__ == "__main__":
	asyncio.run(run())