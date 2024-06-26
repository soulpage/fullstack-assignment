# chat/urls.py
from django.urls import path
from .views import (
    chat_root_view,
    get_conversations,
    get_conversations_branched,
    get_conversation_branched,
    add_conversation,
    conversation_manage,
    conversation_change_title,
    conversation_add_message,
    conversation_add_version,
    conversation_switch_version,
    conversation_soft_delete,
    version_add_message,
    ConversationListView,
    FileUploadView,
    UploadedFileListView,
    FileDeleteView
)

urlpatterns = [
    path("", chat_root_view, name="chat_root_view"),
    path("conversations/", get_conversations, name="get_conversations"),
    path("conversations_branched/", get_conversations_branched, name="get_branched_conversations"),
    path("conversation_branched/<uuid:pk>/", get_conversation_branched, name="get_branched_conversation"),
    path("conversations/add/", add_conversation, name="add_conversation"),
    path("conversations/<uuid:pk>/", conversation_manage, name="conversation_manage"),
    path("conversations/<uuid:pk>/change_title/", conversation_change_title, name="conversation_change_title"),
    path("conversations/<uuid:pk>/add_message/", conversation_add_message, name="conversation_add_message"),
    path("conversations/<uuid:pk>/add_version/", conversation_add_version, name="conversation_add_version"),
    path(
        "conversations/<uuid:pk>/switch_version/<uuid:version_id>/",
        conversation_switch_version,
        name="conversation_switch_version",
    ),
    path("conversations/<uuid:pk>/delete/", conversation_soft_delete, name="conversation_delete"),
    path("versions/<uuid:pk>/add_message/", version_add_message, name="version_add_message"),
    path('conversations/', ConversationListView.as_view(), name='conversation-list'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('files/', UploadedFileListView.as_view(), name='file-list'),
    path('files/<uuid:pk>/', FileDeleteView.as_view(), name='file-delete'),
]
