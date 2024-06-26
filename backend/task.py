from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Conversation

@shared_task
def cleanup_old_conversations(days):
    threshold_date = timezone.now() - timedelta(days=days)
    old_conversations = Conversation.objects.filter(created__lt=threshold_date)
    old_conversations.delete()
