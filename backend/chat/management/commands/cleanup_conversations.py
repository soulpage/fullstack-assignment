from django.core.management.base import BaseCommand
from chat.models import Conversation
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Clean up old conversations'

    def handle(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(days=30)
        old_conversations = Conversation.objects.filter(created__lt=threshold_date)
        count = old_conversations.count()
        old_conversations.delete()
        self.stdout.write(f'Successfully deleted {count} old conversations.')
