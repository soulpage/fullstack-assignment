from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.management import call_command

@shared_task
def cleanup_old_conversations(days=30):
    call_command('cleanup_old_conversations', '--days', str(days))
