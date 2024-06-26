from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from chat.models import Conversation

#Implemented a management command to clean up old conversations.
class Command(BaseCommand):
    help = 'Cleanup old conversations'

    def handle(self, *args, **kwargs):
        cutoff_date = datetime.now() - timedelta(days=30)
        old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
        count = old_conversations.count()
        old_conversations.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} old conversations'))
