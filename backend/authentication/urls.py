from django.urls import path
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, FileUploadViewSet
from authentication import views

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'file-uploads', FileUploadViewSet)

urlpatterns = [
    path("", views.auth_root_view, name="auth_root"),
    path("csrf_token/", views.csrf_token, name="csrf_token"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("verify_session/", views.verify_session, name="verify_session"),
    path('', include(router.urls)),

]
