"""
URL configuration for assignment2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp.views import ConversationViewSet
from myapp.views import FileUploadView, FileListView, FileDeleteView


router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/files/', FileListView.as_view(), name='file-list'),
    path('api/files/<int:file_id>/', FileDeleteView.as_view(), name='file-delete'),
]
