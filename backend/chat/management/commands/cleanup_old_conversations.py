import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from chat.models import Conversation

class Command(BaseCommand):
    help = 'Clean up old conversation'

    def add_arguments(self,parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Specify the age of conversations to delete in days'
        )
        parser.add_argument(
            '--use-created-at',
            action='store_true',
            help = 'use created_at date instead of modified_at date to determine old conversations'
        )

    def handle(self,*args,**options):
        days = options['days']
        use_created_at = options['use_created_at']
        threshold_date = timezone.now() - datetime.timedelta(days=days)

        if use_created_at:
            old_conversations = Conversation.objects.filter(created_at=threshold_date)
        else:
            old_conversations = Conversation.objects.filter(modified_at=threshold_date)
        
        count = old_conversations.count()
        old_conversations.delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} old conversations'))