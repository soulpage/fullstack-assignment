from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from your_app.models import Conversation

@shared_task
def cleanup_old_conversations():
    cutoff_date = timezone.now() - timedelta(days=30)
    old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
    old_conversations.delete()
