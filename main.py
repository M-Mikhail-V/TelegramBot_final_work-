import sys

from aiogram import Dispatcher, Bot
from aiogram.types import BotCommand
from dotenv import load_dotenv
import asyncio
import os
import logging
from aiogram_dialog import setup_dialogs
from utils.models import Users, Services, Appointments
from handlers.start import start_router
from handlers.registration import registration_router
from handlers.get_appointment import appointment_router
from handlers.admin import admin_router


load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()

dp.include_routers(start_router, registration_router, appointment_router, admin_router)
setup_dialogs(dp)


async def main():
    tables = [Users, Appointments, Services]
    for table in tables:
        if not table.table_exists():
            table.create_table()
    print('started')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    await bot.set_my_commands([BotCommand(command='start', description='Главное меню')])
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit Bot')
