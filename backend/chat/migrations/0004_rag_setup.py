from django.db import migrations
from rag.models import KnowledgeBase

def load_knowledge_base(apps, schema_editor):
    # Generating rag for a chatbot
    data = [
      ("What is your name?", "I am a chatbot."),
      ("Always answer bubly and in a rhythmic way")
    ]

    KnowledgeBase = apps.get_model("rag", "KnowledgeBase")
    for text, embedding in data:
        KnowledgeBase.objects.create(text=text, embedding=embedding)

def reverse_func(apps, schema_editor):
    KnowledgeBase = apps.get_model("rag", "KnowledgeBase")
    KnowledgeBase.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(load_knowledge_base, reverse_func),
    ]