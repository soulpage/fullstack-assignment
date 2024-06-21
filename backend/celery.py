from __future__ import absolute_import,unicode_literals
import os
from celery import Celery

#set the default Django settings module for the celery program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')

#create a celery instance.
app = Celery('backend')

#load task module from all registered django app configs.
app.config_from_objects('django.conf:settings',namespace='CELERY')

#Auto-discover tasks in all apps
app.autodiscover_tasks()