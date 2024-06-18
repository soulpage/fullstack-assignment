from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat import views

# Router for conversation ViewSet
router = DefaultRouter()
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

# Define URL patterns
urlpatterns = [
    path('', views.chat_root_view, name='chat_root_view'),
    path('conversations/', views.get_conversations, name='get_conversations'),
    path('conversations_branched/', views.get_conversations_branched, name='get_branched_conversations'),
    path('conversation_branched/<uuid:pk>/', views.get_conversation_branched, name='get_branched_conversation'),
    path('conversations/add/', views.add_conversation, name='add_conversation'),
    path('conversations/<uuid:pk>/', views.conversation_manage, name='conversation_manage'),
    path('conversations/<uuid:pk>/change_title/', views.conversation_change_title, name='conversation_change_title'),
    path('conversations/<uuid:pk>/add_message/', views.conversation_add_message, name='conversation_add_message'),
    path('conversations/<uuid:pk>/add_version/', views.conversation_add_version, name='conversation_add_version'),
    path('conversations/<uuid:pk>/switch_version/<uuid:version_id>/', views.conversation_switch_version, name='conversation_switch_version'),
    path('conversations/<uuid:pk>/delete/', views.conversation_soft_delete, name='conversation_delete'),
    path('versions/<uuid:pk>/add_message/', views.version_add_message, name='version_add_message'),

    # File management endpoints
    path('upload-file/', views.upload_file, name='upload_file'),
    path('list-uploaded-files/', views.list_uploaded_files, name='list_uploaded_files'),
    path('delete-uploaded-file/<int:pk>/', views.delete_uploaded_file, name='delete_uploaded_file'),

    # Include Django's authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),

    # Include the router URLs
    path('', include(router.urls)),

    # RAGData endpoints
    path('rag-data/', views.RAGDataListView.as_view(), name='rag-data-list'),
    path('rag-data/<int:pk>/', views.RAGDataDetailView.as_view(), name='rag-data-detail'),
]
