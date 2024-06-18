# chat/management/commands/cleanup_old_conversations.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from chat.models import Conversation

class Command(BaseCommand):
    help = 'Clean up old conversations'

    def handle(self, *args, **kwargs):
        # Define your cleanup logic here
        old_conversations = Conversation.objects.filter(deleted_at__lte=timezone.now() - timezone.timedelta(days=30))
        count, _ = old_conversations.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old conversations.'))
