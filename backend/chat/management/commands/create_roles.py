from django.core.management.base import BaseCommand
from chat.models import Conversation  # Ensure this is the correct path to your Conversation model
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes conversations older than a specified number of days'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, help='The number of days to keep conversations')

    def handle(self, *args, **kwargs):
        days = kwargs['days']
        threshold_date = timezone.now() - timedelta(days=days)
        old_conversations = Conversation.objects.filter(created_at__lt=threshold_date)  # Use created_at instead of created
        count = old_conversations.count()
        old_conversations.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} conversations'))
