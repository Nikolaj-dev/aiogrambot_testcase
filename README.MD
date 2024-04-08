Инструкция к проекту

Проект представляет собой Django-приложение с встроенным телеграм-ботом и фоновыми задачами, использующими Celery.

Установка

1. Склонируйте репозиторий:

   git clone *https://github.com/Nikolaj-dev/aiogrambot_testcase*

2. Создайте виртуальное окружение и активируйте его:

   python -m venv env

   call env/scripts/activate  # Для Windows

   source env/bin/activate # Для Linux

3. Установите зависимости:

   pip install -r requirements.txt

4. Создайте файл .env:

   Используйте пример в файле env_instance.txt для заполнения необходимых полей(проект использует Redis и PostgreSQL).

Запуск
1. Выполните миграции
   python manage.py migrate

2. Запустите сервер Django:

   python manage.py runserver

3. Запустите телеграм-бот:

   python manage.py runbot

4. Запустите Celery для выполнения фоновых задач:

   celery -A django_conf worker -l info -P threads

5. Запустите Celery для выполнения рассылки курса валюты:

   celery -A django_conf beat -l info

Каждую команду запускайте поочередно в указанной последовательности.

После выполнения этих шагов ваш проект должен быть успешно запущен, и вы готовы к использованию.
