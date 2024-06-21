import uuid

from django.db import models

from authentication.models import CustomUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.html import strip_tags
from gensim.summarization import summarize
import hashlib

class Role(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, default="user")

    def __str__(self):
        return self.name


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100, blank=False, null=False, default="Mock title")
    summary = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active_version = models.ForeignKey(
        "Version", null=True, blank=True, on_delete=models.CASCADE, related_name="current_version_conversations"
    )
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def version_count(self):
        return self.versions.count()

    version_count.short_description = "Number of versions"

    def generate_summary(self):
        """
        Automatically generates a summary based on the content using gensim.
        """
        if self.title:
            cleaned_content = strip_tags(self.title).strip()
            
            # Check if the cleaned content has more than one sentence
            if len(cleaned_content.split('.')) > 1:
                summarized_text = summarize(cleaned_content, ratio=0.2)  # Adjust ratio or word_count as needed
                self.summary = summarized_text
            else:
                self.summary = "Content is too short for summarization"
        else:
            self.summary = "No content available"

    def save(self, *args, **kwargs):
        # Call generate_summary only if summary is empty or needs to be regenerated
        if not self.summary:
            self.generate_summary()
        super().save(*args, **kwargs)

@receiver(pre_save, sender=Conversation)
def generate_summary(sender, instance, **kwargs):
    """
    Signal receiver function to generate summary before saving Conversation instance.
    """
    instance.generate_summary()


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
    

def user_directory_path(instance, filename):
    return f'user_{instance.user.id}/{filename}'

class FileUpload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_directory_path)
    checksum = models.CharField(max_length=64, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.checksum:
            self.checksum = self.generate_checksum()
        super().save(*args, **kwargs)

    def generate_checksum(self):
        sha256 = hashlib.sha256()
        self.file.seek(0)
        for chunk in iter(lambda: self.file.read(4096), b""):
            sha256.update(chunk)
        return sha256.hexdigest()
