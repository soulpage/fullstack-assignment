from django_filters import rest_framework as filters

from chat.models import Conversation

class ConversationSummaryFilter(filters.FilterSet):
    class Meta:
        model = Conversation
        fields = {
            'title': ['iexact', 'icontains'], 
            'summary': ['iexact', 'icontains']
        }