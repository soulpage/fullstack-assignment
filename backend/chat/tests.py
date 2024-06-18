from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from chat.models import Conversation, Message

class ConversationTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        
        self.conversation = Conversation.objects.create(title='Test Conversation', user=self.user)
        self.message = Message.objects.create(content='Hello', conversation=self.conversation)

    def test_get_conversations(self):
        url = reverse('get-conversations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Assuming there's one conversation in setup

    def test_add_conversation(self):
        url = reverse('add-conversation')
        data = {'title': 'New Conversation', 'messages': [{'content': 'Message 1'}]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversation.objects.count(), 2)  # Check if conversation count increased

    def test_delete_conversation(self):
        url = reverse('conversation-manage', kwargs={'pk': self.conversation.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Conversation.objects.count(), 0)  # Check if conversation was deleted

    def test_permissions(self):
        unauthorized_client = APIClient()
        url = reverse('add-conversation')
        data = {'title': 'New Conversation', 'messages': [{'content': 'Message 1'}]}
        
        # Ensure unauthorized access is forbidden
        response = unauthorized_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
