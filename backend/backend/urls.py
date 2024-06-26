from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.decorators import api_view


@api_view(["GET"])
def root_view(request):
    return JsonResponse({"message": "App works!"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path("gpt/", include("gpt.urls")),
    path("auth/", include("authentication.urls")),
    path("", root_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
