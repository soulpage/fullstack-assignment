import uuid

from django.db import models
import os
from authentication.models import CustomUser
import openai
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
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

    def generate_summary(self):
        try:
            messages = self.messages.all()
            text = " ".join([msg.content for msg in messages])
            openai.api_key = OPENAI_API_KEY  
            response = openai.Completion.create(
                model="text-davinci-003",  
                prompt=f"Generate summary:\n{text}",  
                max_tokens=150  
            )
            self.summary = response.choices[0].text.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
        self.save()

    def save(self, *args, **kwargs):
        
        if not self.summary:
            self.generate_summary()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def version_count(self):
        return self.versions.count()

    version_count.short_description = "Number of versions"


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


import hashlib

class File(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    hash = models.CharField(max_length=32, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate hash of the file before saving
        if not self.hash:
            self.hash = self.calculateFileHash()
        super().save(*args, **kwargs)

    def calculateFileHash(self):
        # Calculate hash of the file
        file_hash = hashlib.md5()
        with open(self.path, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for chunk in iter(lambda: f.read(4096), b""):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def delete(self, *args, **kwargs):
        # Delete the file from the filesystem
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
