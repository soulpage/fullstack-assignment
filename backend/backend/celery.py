# celery.py or tasks.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

from celery.schedules import crontab

# Using RabbitMQ as the message broker
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'cleanup-old-conversations': {
        'task': 'chat.tasks.cleanup_old_conversations_task',
        'schedule': crontab(hour=0, minute=0),  # Daily at midnight
    },
}