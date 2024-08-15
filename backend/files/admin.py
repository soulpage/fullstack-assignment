from django.contrib import admin
from nested_admin.nested import NestedModelAdmin

from files.models import File

# Register your models here.

class FileAdmin(NestedModelAdmin):
    list_display = ("id", "file", "user", "uploaded_at")
    ordering = ("-uploaded_at",)

admin.site.register(File, FileAdmin)