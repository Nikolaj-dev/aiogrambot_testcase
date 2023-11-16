import asyncio
import requests
from aiogram.enums import ParseMode
from celery import shared_task
from .models import TelegramChat
from .bot import bot
from django_conf.celery import app
from asgiref.sync import async_to_sync, sync_to_async


@app.task
def send_course():
    url = ''



