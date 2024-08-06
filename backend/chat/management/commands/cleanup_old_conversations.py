from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from chat.models import Conversation

class Command(BaseCommand):
    help = 'Delete conversations older than a specified number of days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Specify the age of conversations to delete (default is 30 days)',
        )

    def handle(self, *args, **options):
        days = options['days']
        threshold_date = datetime.now() - timedelta(days=days)
        old_conversations = Conversation.objects.filter(created_at__lt=threshold_date)
        count = old_conversations.count()
        old_conversations.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} conversations older than {days} days'))
