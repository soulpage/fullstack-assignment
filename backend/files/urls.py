from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from files import views


urlpatterns = [
    path("", views.get_files, name="get_files"),
    path("upload/", views.upload_file, name="upload_file"),
    path("<uuid:pk>/delete/", views.delete_file, name="delete_file"),
] 