from django.core.management.base import BaseCommand
from ....chat.models import Conversation
from datetime import datetime, timedelta

# This class helps to delete old conversations
class Command(BaseCommand):
    help = 'Deletes conversations older than 30 days'

    def handle(self, *args, **kwargs):
        threshold_date = datetime.now() - timedelta(days=30)
        old_conversations = Conversation.objects.filter(created_at__lt=threshold_date)
        old_conversations.delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted old conversations'))z