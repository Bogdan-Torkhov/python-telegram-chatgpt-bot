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

user_messages = {}

def update(user_id, role, content):
    if user_id not in user_messages:
        user_messages[user_id] = [
            {"role": "system", "content": "You are a chat bot powered by gpt-4 model"}
        ]
    user_messages[user_id].append({"role": role, "content": content}) 

@dp.message_handler(commands=['start'])
async def welcome_command(message: types.Message):
    await message.answer("Что нужно решить? Cоздано Богданом Торховым")


@dp.message_handler()
async def send(message: types.Message):
    update(message.from_user.id, "user", message.text)
    openai.api_key = os.getenv("API_KEY_OPENAI")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=user_messages[message.from_user.id]
    )
    user_messages[message.from_user.id].append({
        "role": "assistant", 
        "content": response['choices'][0]['message']['content']
    })
    await message.answer(response['choices'][0]['message']['content'], parse_mode=types.ParseMode.MARKDOWN)
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')


if __name__ == '__main__':
    executor.start_polling(dp)
