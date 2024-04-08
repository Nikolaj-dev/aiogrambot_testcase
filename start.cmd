@echo off
start cmd /k "python -m venv env && call env\scripts\activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver"
start cmd /k "call env\scripts\activate && python manage.py runbot"
start cmd /k "call env\scripts\activate && celery -A django_conf worker -l info -P threads"
start cmd /k "call env\scripts\activate && celery -A django_conf beat -l info"
