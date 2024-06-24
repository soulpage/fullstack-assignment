# conversations/admin.py

from django.contrib import admin
from .models import Conversation

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id','title','transcript', 'summary')
