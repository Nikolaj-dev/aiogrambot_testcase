import asyncio
import json
import logging

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse, HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt

from .bot import bot
from .models import TelegramChat, CurrencyHistory


@csrf_exempt
def get_currency(request: HttpRequest) -> JsonResponse:
    url = 'https://www.floatrates.com/daily/usd.json'
    response = requests.get(url=url)
    if response.status_code == 200:
        json_data = response.json()
        rub_data = json_data.get("rub")
        if rub_data:
            course = {
                "Currency Code": rub_data["code"],
                "Name": rub_data["name"],
                "Exchange Rate": rub_data["rate"],
                "Date": rub_data["date"],
                "Inverse Rate": rub_data["inverseRate"],
            }
            if request.method == 'GET':
                return JsonResponse(course, safe=False)
            if request.headers.get('content-type') == 'application/json':
                try:
                    # Получение JSON-данных из запроса
                    json_data = json.loads(request.body.decode('utf-8'))
                    username = json_data["username"]
                    try:
                        user = User.objects.filter(
                            username=str(username),
                        ).first()
                        if user:
                            CurrencyHistory.objects.create(
                                user=user,
                                code=course.get('Currency Code'),
                                name=course.get('Name'),
                                rate=course.get('Exchange Rate'),
                                date=course.get('Date'),
                                inverseRate=course.get('Inverse Rate')
                            )
                            return JsonResponse({"message": "Готово!"}, status=200)
                    except Exception as e:
                        logging.error(f"Error: {e}", exc_info=True)
                        return JsonResponse({"message": "Упс... Что-то пошло не так."}, status=500)
                except json.JSONDecodeError:
                    return JsonResponse({"message": 'Invalid JSON data'}, status=400)
                except Exception as e:
                    logging.error(f"Error: {e}", exc_info=True)
                    return JsonResponse({"message": "Ошибка сервера!"}, status=500)
            else:
                return JsonResponse({"message": 'Request must be in JSON format'}, status=400)

    else:
        return JsonResponse({"message": "error 500"}, safe=False)


@csrf_exempt
def register(request: HttpRequest) -> JsonResponse:
    if request.headers.get('content-type') == 'application/json':
        try:
            # Получение JSON-данных из запроса
            json_data = json.loads(request.body.decode('utf-8'))
            username = json_data["username"]
            password = User.objects.make_random_password()
            chat_id = json_data["chat_id"]
            try:
                user = User.objects.create(
                    username=str(username),
                    password=password
                )
                if user:
                    try:
                        TelegramChat.objects.create(
                            chat_id=str(chat_id),
                            user=user
                        )
                        return JsonResponse({"message": "Готово!"}, status=200)
                    except Exception as e:
                        logging.error(f"Error: {e}", exc_info=True)
                        return JsonResponse({"message": "Ошибка!"}, status=200)
                else:
                    return JsonResponse({"message": "Ошибка!"}, status=200)
            except Exception as e:
                logging.error(f"Error: {e}", exc_info=True)
                return JsonResponse({"message": "Упс... возможно вы уже зарегистрированны."}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({"message": 'Invalid JSON data'}, status=400)
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)
            return JsonResponse({"message": "Ошибка сервера!"}, status=500)
    else:
        return JsonResponse({"message": 'Request must be in JSON format'}, status=400)


@csrf_exempt
def history(request: HttpRequest) -> JsonResponse:
    if request.headers.get('content-type') == 'application/json':
        try:
            # Получение JSON-данных из запроса
            json_data = json.loads(request.body.decode('utf-8'))
            username = json_data["username"]
            try:
                user = User.objects.get(
                    username=str(username),
                )
                history_data = CurrencyHistory.objects.filter(user=user)
                data = []
                for i in range(len(history_data)):
                    obj = history_data[i]
                    data.append({
                            "Валюта": obj.code,
                            "Курс": str(obj.rate)[0:4],
                            "Время": obj.created_at
                        })
                return JsonResponse({"message": data}, status=200)
            except Exception as e:
                logging.error(f"Error: {e}", exc_info=True)
                return JsonResponse({"message": "Упс... Что-то пошло не так."}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({"message": 'Invalid JSON data'}, status=400)
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)
            return JsonResponse({"message": "Ошибка сервера!"}, status=500)
    else:
        return JsonResponse({"message": 'Request must be in JSON format'}, status=400)


@csrf_exempt
def subscribe(request: HttpRequest) -> JsonResponse:
    if request.headers.get('content-type') == 'application/json':
        try:
            # Получение JSON-данных из запроса
            json_data = json.loads(request.body.decode('utf-8'))
            username = json_data["username"]
            chat = TelegramChat.objects.get(user__username=str(username))
            if chat.subscribed == False:
                chat.subscribed = True
                chat.save()
                return JsonResponse({"message": "Вы успешно подписались."}, status=200)
            else:
                return JsonResponse({"message": "Вы уже подписаны!"}, status=400)
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)
            return JsonResponse({"message": "Ошибка сервера."}, status=500)
    else:
        pass

@csrf_exempt
def unsubscribe(request: HttpRequest) -> JsonResponse:
    if request.headers.get('content-type') == 'application/json':
        try:
            # Получение JSON-данных из запроса
            json_data = json.loads(request.body.decode('utf-8'))
            username = json_data["username"]
            chat = TelegramChat.objects.get(user__username=str(username))
            if chat.subscribed == True:
                chat.subscribed = False
                chat.save()
                return JsonResponse({"message": "Вы успешно отписались."}, status=200)
            else:
                return JsonResponse({"message": "Вы уже отписаны!"}, status=400)
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)
            return JsonResponse({"message": "Ошибка сервера."}, status=500)
    else:
        pass


def mailing(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        async def body():
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
                        await bot.send_message(chat_id=chat.chat_id, text=text)

        return JsonResponse({"message": "200"}, status=200)
