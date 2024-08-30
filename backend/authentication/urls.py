from django.urls import path

from authentication import views

start_http_server(8001)

urlpatterns = [
    path("", views.auth_root_view, name="auth_root"),
    path("csrf_token/", views.csrf_token, name="csrf_token"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("verify_session/", views.verify_session, name="verify_session"),
]
