from .models import TelegramChat
from .bot import bot
import requests


def send_beat_course():
    for chat in TelegramChat.objects.filter(subscribed=True):
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
                text = f"Курс рубля от {course.get('Date')}: 1 USD = {str(course.get('Exchange Rate'))[0:4]} {course.get('Currency Code')}"
                bot.send_message(chat_id=chat.chat_id, text=text)