import logging
import os
import sys

from aiogram.utils import executor
from create_bot import bot, dp
from data_base import sqlite_db
from dotenv import load_dotenv
from errors import ErrorsText
from handlers import admin
from handlers.admin import set_default_commands

load_dotenv()
admin.register_handlers_admin(dp)

WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')
WEBHOOK_PATH = '/webhook/{bot}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

"""Создаем логгер."""
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)


async def on_startup(_):
    logger.info('Бот запущен')
    try:
        await bot.set_webhook(WEBHOOK_URL)
        await set_default_commands(dp)
    except Exception:
        raise ErrorsText('Ошибка Запуска бота')
    sqlite_db.sql_start()


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
