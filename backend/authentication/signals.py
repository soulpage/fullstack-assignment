from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Conversation
from .utils import generate_summary  # Import a utility function to generate summaries

@receiver(post_save, sender=Conversation)
def generate_and_store_summary(sender, instance, **kwargs):
    if kwargs.get('created', False):  # this will only generate summary for new instances
        summary = generate_summary(instance)
        instance.summary = summary
        instance.save()
