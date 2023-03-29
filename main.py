import os
import logging
import openai
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
import time

# loading env variables
load_dotenv()
# info logging
logging.basicConfig(level=logging.INFO)

# telegram bot block
telegram_token = os.getenv("API_KEY_TELEGRAM")
bot = Bot(token=telegram_token)
dp = Dispatcher(bot=bot)

messages = [
    {"role": "system", "content": "You are chat-bot powered by gpt-3.5-turbo model"},
    {"role": "user", "content": "any question"},
    {"role": "assistant", "content": "You are assistant"}
]


def update(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages


@dp.message_handler(commands=['start'])
async def welcome_command(message: types.Message):
    await message.answer("Что нужно решить? Cоздано Богданом Торховым")


@dp.message_handler()
async def send(message: types.Message):
    update(messages, "user", message.text)
    openai.api_key = os.getenv("API_KEY_OPENAI")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    await message.answer(response['choices'][0]['message']['content'])
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')


if __name__ == '__main__':
    executor.start_polling(dp)
