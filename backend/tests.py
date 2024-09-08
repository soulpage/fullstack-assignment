from django.test import TestCase
from .models import Conversation
from .utils import generate_summary

class ConversationModelTest(TestCase):
    def setUp(self):
        self.conversation = Conversation.objects.create(content="Test content")

    def test_summary_generation(self):
        # Assuming generate_summary sets a summary based on content
        self.conversation.summary = generate_summary(self.conversation)
        self.conversation.save()
        self.assertEqual(self.conversation.summary, "Generated summary based on content")
