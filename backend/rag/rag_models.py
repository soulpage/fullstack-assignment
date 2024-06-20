#Importing models from django
from django.db import models

class KnowledgeBase(models.Model):
    text = models.TextField()
    embedding = models.BinaryField()

    def __str__(self):
        return f"{self.text[:50]}..."