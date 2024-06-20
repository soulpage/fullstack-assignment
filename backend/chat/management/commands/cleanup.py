
from django.core.management.base import BaseCommand
from django.utils import timezone
from chat.models import Conversation  

class Command(BaseCommand):
    help = 'Clean up old conversations'

    def handle(self, *args, **kwargs):

        cutoff_date = timezone.now() - timezone.timedelta(days=30)
        
        deleted_count, _ = Conversation.objects.filter(modified_at__lt=cutoff_date).delete()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {deleted_count} old conversations.'))
