from django.contrib import admin
from django.utils import timezone
from django.template.defaultfilters import truncatechars
from .models import Conversation

class DeletedListFilter(admin.SimpleListFilter):
    title = "Deleted"
    parameter_name = "deleted"

    def lookups(self, request, model_admin):
        return (
            ("True", "Yes"),
            ("False", "No"),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == "True":
            return queryset.filter(deleted_at__isnull=False)
        elif value == "False":
            return queryset.filter(deleted_at__isnull=True)
        return queryset

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    actions = ["undelete_selected", "soft_delete_selected"]
    list_display = (
        "title", "id", "created_at", "modified_at", "deleted_at", "version_count", "is_deleted", "user", "summary"
    )
    list_filter = (DeletedListFilter, "deleted_at")
    search_fields = ("title",)

    def undelete_selected(self, request, queryset):
        queryset.update(deleted_at=None)

    undelete_selected.short_description = "Undelete selected conversations"

    def soft_delete_selected(self, request, queryset):
        queryset.update(deleted_at=timezone.now())

    soft_delete_selected.short_description = "Soft delete selected conversations"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related("messages")  # Prefetch related messages for efficiency
        return queryset

    def is_deleted(self, obj):
        return obj.deleted_at is not None

    is_deleted.boolean = True
    is_deleted.short_description = "Deleted?"

    def summary(self, obj):
        if obj.messages.exists():
            messages_preview = "\n".join([message.content for message in obj.messages.all()])
            return truncatechars(messages_preview, 100)
        else:
            return "No messages"

    summary.short_description = "Summary"
