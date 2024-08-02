from django.core.management.base import BaseCommand
from ...models import Conversation
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Clean up old conversations'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timedelta(days=30)  # Adjust the time period as needed
        old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
        count, _ = old_conversations.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old conversations'))
