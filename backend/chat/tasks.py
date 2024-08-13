from celery import shared_task

from django.core.management import call_command

@shared_task
def cleanup_old_conversation_task(*args, **kwargs):
    call_command('cleanup_old_conversations', days=kwargs['days'], hours=kwargs['hours'])