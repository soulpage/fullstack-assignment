from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    'cleanup-old-conversations': {
        'task': 'conversations.tasks.cleanup_old_conversations',
        'schedule': crontab(hour=0, minute=0),
        'args': (30,),
    },
}
