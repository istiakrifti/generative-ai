import logging
import os
from dotenv import load_dotenv 
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# print(TELEGRAM_BOT_TOKEN)

#configuire logging
logging.basicConfig(level=logging.INFO)

#initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.message):
    """
    This handler receives messages with `/start` or `/help` command
    """
    await message.answer(f"Hello\nI am an Echo Bot\nPowered by aiogram")

@dp.message_handler()
async def echo(message: types.message):
    """
    This will return echo
    """
    await message.answer(message.text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)