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


@dp.message_handler(commands=['start'])
async def welcome_command(message: types.Message):
    await message.answer("Что нужно решить? Cоздано Богданом Торховым")


@dp.message_handler()
async def answer(message: types.Message):

    openai.api_key = os.getenv("API_KEY_OPENAI")

    model_engine = "text-davinci-003"

    response = openai.Completion.create(
        model=model_engine,
        prompt=message.text,
        max_tokens=1024,
        temperature=1,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1,
        n=1,
    )

    answer_to_your_question = response.choices[0].text

    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id=} {user_full_name=} {time.asctime()}')
    await message.reply(answer_to_your_question)


if __name__ == '__main__':
    executor.start_polling(dp)
