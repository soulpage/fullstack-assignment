
from django.core.management.base import BaseCommand
from django.utils import timezone
from chat.models import Conversation  # Replace with your actual Conversation model

class Command(BaseCommand):
    help = 'Cleanup old conversations'

    def handle(self, *args, **kwargs):
        # Define the age limit for conversations to delete (e.g., older than 30 days)
        age_limit = timezone.now() - timezone.timedelta(days=30)
        
        # Query and delete conversations older than the age limit
        deleted_count, _ = Conversation.objects.filter(created_at__lt=age_limit).delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} old conversations'))
