# conversations/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Conversation

@receiver(post_save, sender=Conversation)
def generate_summary(sender, instance, **kwargs):
    if not instance.summary:
        instance.summary = "Generated summary"  # Replace with actual summary generation logic
        instance.save()
