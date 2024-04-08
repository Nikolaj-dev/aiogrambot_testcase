@echo off
start cmd /k "call env\scripts\activate && pip install -r requirements.txt && python manage.py migrate"