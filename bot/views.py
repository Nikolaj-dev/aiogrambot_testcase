import json
import logging
from django.contrib.auth.models import User
from django.http import HttpRequest, JsonResponse
from .service import get_course
from django.views.decorators.csrf import csrf_exempt
from .models import TelegramChat, CurrencyHistory


@csrf_exempt
def get_currency(request: HttpRequest) -> JsonResponse:
    course = get_course()
    if request.method == 'GET':
        return JsonResponse(course, safe=False)
    if request.method == 'POST':
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
                        try:
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
                            return JsonResponse({"message": "Ошибка получения истории запросов."}, status=500)
                    else:
                        return JsonResponse({"message": "Пользователь пока не зарегистрировался."}, status=200)
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
                        return JsonResponse({"message": "Ошибка регистрации чата."}, status=500)
                else:
                    return JsonResponse({"message": "Ошибка! Пользователь не найден."}, status=400)
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
