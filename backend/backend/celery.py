from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
from celery import Celery
from celery.schedules import crontab

app = Celery('your_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'cleanup-old-conversations': {
        'task': 'your_app.tasks.cleanup_old_conversations',
        'schedule': crontab(hour=0, minute=0),
    },
}
