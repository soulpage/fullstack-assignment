from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from your_app.models import Conversation

class Command(BaseCommand):
    help = 'Deletes conversations older than a specified number of days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Specify the number of days to keep conversations',
        )

    def handle(self, *args, **kwargs):
        days = kwargs['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        old_conversations = Conversation.objects.filter(created_at__lt=cutoff_date)
        count, _ = old_conversations.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} conversations older than {days} days'))
