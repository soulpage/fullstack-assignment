# conversations/models.py

from django.db import models
from django.utils.text import Truncator

class Conversation(models.Model):
    title = models.CharField(max_length=100)
    transcript = models.TextField()
    summary = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        summary = Truncator(self.transcript).words(30, truncate='...')
        self.summary = summary
        super().save(*args, **kwargs)
