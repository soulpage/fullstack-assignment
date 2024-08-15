import uuid

from django.db import models

from authentication.models import CustomUser


class Role(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, default="user")

    def __str__(self):
        return self.name


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False, default="Mock title")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active_version = models.ForeignKey(
        "Version", null=True, blank=True, on_delete=models.CASCADE, related_name="current_version_conversations"
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def version_count(self):
        return self.versions.count()

    version_count.short_description = "Number of versions"

    def save(self, *args, **kwargs):
        # Save summary, if no summary exists.
        if not self.summary:
            self.summary = self.generate_summary()
        super().save(*args, **kwargs)

    def generate_summary(self):
        summary = ""

        # Returns empty string if no version exists.
        if not self.versions.exists():
            return summary
        
        # Get all the messages of version #1.
        messages = self.versions.first().messages.all()

        # For every message, add role name and the message content.
        message_text = ""
        for message in messages:
            message_text += f"{message.role.name}: {message.content}\n"
        
        # Length of summary to limited to 100 characters.
        summary = message_text[:100]

        return summary

class Version(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey("Conversation", related_name="versions", on_delete=models.CASCADE)
    parent_version = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    root_message = models.ForeignKey(
        "Message", null=True, blank=True, on_delete=models.SET_NULL, related_name="root_message_versions"
    )

    def __str__(self):
        if self.root_message:
            return f"Version of `{self.conversation.title}` created at `{self.root_message.created_at}`"
        else:
            return f"Version of `{self.conversation.title}` with no root message yet"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(blank=False, null=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.ForeignKey("Version", related_name="messages", on_delete=models.CASCADE)

    class Meta:
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        self.version.conversation.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.role}: {self.content[:20]}..."
