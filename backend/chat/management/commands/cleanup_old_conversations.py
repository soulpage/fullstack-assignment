from django.core.management.base import BaseCommand, CommandParser, CommandError
from django.utils import timezone
from datetime import timedelta

from chat.models import Conversation

class Command(BaseCommand):
    help = "Cleanup conversations which were last modified before specified number of days or hours."

    # Last Modified in hours. Default argument 24 hours.
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--days',
            type=int,
            default=1,
            help='Specify number of days old conversations to be deleted (default: 1 day)'
        )

        parser.add_argument(
            '--hours',
            type=int,
            default=0,
            help='Specify number of hours old conversations to be deleted (default: 0 hour)'
        )

    def handle(self, *args, **options):
        days = options['days']
        hours = options['hours']
        self.stdout.write(self.style.HTTP_INFO(f'Conversations older than {days}d {hours}h will be deleted.'))
        stipulated_datetime = timedelta(days=days, hours=hours)
        old_conversations = Conversation.objects.filter(
            modified_at__lte=timezone.now()-stipulated_datetime
        )
        count = old_conversations.count()
        if count:
            old_conversations.delete()
            self.stdout.write(self.style.SUCCESS(f'{count} conversation(s) deleted.'))
        else:
            self.stdout.write(self.style.WARNING(f'No conversations found older than {days}d {hours}h.'))