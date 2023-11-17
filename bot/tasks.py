import asyncio
import logging
import requests
from aiogram.enums import ParseMode
from celery import shared_task
from .models import TelegramChat
from .bot import bot
from django_conf.celery import app
from asgiref.sync import async_to_sync, sync_to_async




@sync_to_async
def get_chats():
    return list(
        TelegramChat.objects.filter(subscribed=True)
    )


async def send_beat_course():
    chats = await get_chats()
    for chat in chats:
        url = 'https://www.floatrates.com/daily/usd.json'
        response = requests.get(url=url)
        if response.status_code == 200:
            json_data = response.json()
            rub_data = json_data.get("rub")
            if rub_data:
                course = {
                    "Currency Code": rub_data["code"],
                    "Exchange Rate": rub_data["rate"],
                    "Date": rub_data["date"],
                }
                text = f"Курс рубля от {course.get('Date')}\n1 USD = {str(course.get('Exchange Rate'))[0:4]} {course.get('Currency Code')}"
                await bot.send_message(chat_id=chat.chat_id, text=text)


loop = asyncio.get_event_loop()


@app.task
def celery_send_beat_course():
    task = loop.run_until_complete(send_beat_course())
    return task



