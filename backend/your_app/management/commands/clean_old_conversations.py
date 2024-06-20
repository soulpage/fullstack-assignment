from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from chat.models import Conversation



class Command(BaseCommand):
    help = 'Clean up conversations older than a specified number of days'

    def add_arguments(self, parser):
        parser.add_argument('days', type=int, help='Number of days')

    def handle(self, *args, **kwargs):
        days = kwargs['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)

        count = old_conversations.count()
        old_conversations.delete()

        self.stdout.write(self.style.SUCCESS(f'Deleted {count} old conversations'))
