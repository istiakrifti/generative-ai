import logging
import os
from dotenv import load_dotenv 
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
# from aiogram.utils import executor
# import openai
import sys
import ollama
import asyncio

load_dotenv()
# openai.api_key = os.getenv("OpenAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
print(TELEGRAM_BOT_TOKEN)

class Reference:

    """
    A class to store previous response
    """
    def __init__(self) -> None:
        self.response = []


reference = Reference()
# model_name = "gpt-3.5-turbo"


#initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher()

def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = [] 

@dispatcher.message(Command('clear'))
async def clear(message: types.message):
    """
    This handler clears past conversation and context
    """
    clear_past()
    await message.answer(f"I have cleared the past conversation and context")

@dispatcher.message(Command('start'))
async def welcome(message: types.message):
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello!!!\nI am an Echo Bot.\nPowered by aiogram.\nHow can I assist you? To get help use /help command.")

@dispatcher.message(Command('help'))
async def helper(message: types.message):
    """
    This handler displays help menu with `/help` command
    """
    help_command = """
    Hi! I am a telegram bot created by Rifti. Please follow these commands -
    /start - To start a conversation
    /clear - To clear past conversation and context
    /help - To get help 
    I think this helps.
    """
    await message.answer(help_command)

# @dispatcher.message_handler()
# async def chatgpt(message: types.message):
#     """
#     This handler gets connected with api
#     """
#     print(f">>> USER: \n\t{message.text}")
#     response = openai.ChatCompletion.create(
#         model=model_name,
#         messages=[
#             {
#                 "role": "assistant",
#                 "content": reference.response
#             },
#             {
#                 "role": "user",
#                 "content": message.text
#             }
#         ]
#     )
#     reference.response = response['choices'][0]['message']['content']
#     print(f">>> chatGPT: \n\t{reference.response}")
#     await bot.send_message(chat_id=message.chat.id, text=reference.response)

@dispatcher.message(Command('clear'))
async def clear(message: types.message):
    clear_past()
    await message.answer(f"I have cleared the past conversation and context")

@dispatcher.message(Command('start'))
async def welcome(message: types.message):
    await message.answer(f"Hello!!!\nI am an Echo Bot.\nPowered by aiogram.\nHow can I assist you? To get help use /help command.")

@dispatcher.message(Command('help'))
async def helper(message: types.message):
    help_command = """
    Hi! I am a telegram bot created by Rifti. Please follow these commands -
    /start - To start a conversation
    /clear - To clear past conversation and context
    /help - To get help 
    I think this helps.
    """
    await message.answer(help_command)

@dispatcher.message()
async def chat(message: types.message):
    print(f">>> USER: \n\t{message.text}")

    # Add user message to history
    reference.response.append({"role": "user", "content": message.text})

    try:
        response = ollama.chat(model='llama3.2', messages=reference.response)
        assistant_response = response['message']['content']

        # Add assistant response to history
        reference.response.append({"role": "assistant", "content": assistant_response})

        print(f">>> Ollama: \n\t{assistant_response}")
        await bot.send_message(chat_id=message.chat.id, text=assistant_response)
    except Exception as e:
        print(f"Error with Ollama: {e}")
        await message.answer("Sorry, there was an error processing your request.")

async def main():
    await dispatcher.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

# if __name__ == "__main__":
#     executor.start_polling(dispatcher, skip_updates=True)