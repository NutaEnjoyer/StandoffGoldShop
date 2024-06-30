from aiogram.utils import executor

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

bot = Bot(token=config.BOT_TOKEN, parse_mode='HTML', disable_web_page_preview=True)
dp = Dispatcher(bot, storage=MemoryStorage())


async def __on_start_up(dp: Dispatcher) -> None:
    from handlers import register_all_handlers

    register_all_handlers.register(dp)


def start_bot():
    executor.start_polling(dp, skip_updates=True, on_startup=__on_start_up)
