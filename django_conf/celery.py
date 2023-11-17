import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_conf.settings')


app = Celery('django_conf')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-spam-every-1-minute': {
        'task': 'bot.tasks.celery_send_beat_course',
        'schedule': crontab(minute='*/1')
    }
}