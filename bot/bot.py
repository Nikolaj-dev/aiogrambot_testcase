from aiogram import Bot, Dispatcher, types
import logging
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
import requests


logging.basicConfig(level=logging.INFO)
bot = Bot(token='6723625339:AAFLPTBkbDkC568LumYAkAbo5XhM9-t5O-0')

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("started")


@dp.message(Command("register"))
async def register(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    url = 'http://127.0.0.1:8000/bot_api/register/'
    data = {
        "username": f"{username}",
        "chat_id": int(chat_id)
    }
    response = requests.post(url, json=data)
    response_status = response.json().get('message')
    await message.answer(f"{response_status}")


@dp.message(Command("get_currency"))
async def get_currency(message: types.Message):
    url = 'http://127.0.0.1:8000/bot_api/currency/'
    data = {
        "username": f"{message.from_user.username}"
    }
    requests.post(url=url, json=data)

    response = requests.get(url=url)
    json_data = response.json()
    data = {
        "code": json_data.get('Currency Code'),
        "name": json_data.get('Name'),
        "rate": json_data.get('Exchange Rate'),
        "date": json_data.get('Date'),
        "inverseRate": json_data.get('Inverse Rate'),
    }
    await message.answer(f"Курс рубля от {data.get('date')}: 1 USD = {str(data.get('rate'))[0:4]} {data.get('code')}")


@dp.message(Command("history"))
async def history(message: types.Message):
    username = message.from_user.username
    url = 'http://127.0.0.1:8000/bot_api/history/'
    data = {
        "username": f"{username}"
    }
    response = requests.post(url, json=data)
    response_status = response.json().get('message')
    response_list = list(response_status)
    history_text = "\n".join([f"{item['Валюта']}: {item['Курс']} ({item['Время']})" for item in response_list])

    await message.answer(f"История курса валют:\n{history_text}", parse_mode=ParseMode.MARKDOWN)


@dp.message(Command("subscribe"))
async def subscribe(message: types.Message):
    username = message.from_user.username
    url = 'http://127.0.0.1:8000/bot_api/subscribe/'
    data = {
        "username": f"{username}"
    }
    response = requests.post(url, json=data)
    response_text = response.json().get("message")
    await message.answer(f"{response_text}")


@dp.message(Command("unsubscribe"))
async def unsubscribe(message: types.Message):
    username = message.from_user.username
    url = 'http://127.0.0.1:8000/bot_api/unsubscribe/'
    data = {
        "username": f"{username}"
    }
    response = requests.post(url, json=data)
    response_text = response.json().get("message")
    await message.answer(f"{response_text}")


async def main():
    await dp.start_polling(bot)
