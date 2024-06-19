import uuid

from django.db import models

from authentication.models import CustomUser
import openai

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
            # Fetch all messages related to this conversation
            messages = self.messages.all()
            
            # Concatenate all message contents into a single text
            text = " ".join([msg.content for msg in messages])
            
            # Set up OpenAI API key and call OpenAI's Completion endpoint
            openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key
            response = openai.Completion.create(
                model="text-davinci-003",  # Specify the model to use
                prompt=f"Summarize the following conversation:\n{text}",  # Provide the text to summarize
                max_tokens=150  # Limit the length of the summary
            )
            
            # Extract the generated summary from OpenAI's response
            self.summary = response.choices[0].text.strip()
        except Exception as e:
            # Handle exceptions, e.g., log the error
            print(f"Error generating summary: {e}")
        
        # Save the Conversation instance with the generated summary
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


# In models.py
import hashlib

class File(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    hash = models.CharField(max_length=32, unique=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate and set the file hash on save
        if not self.hash:
            self.hash = self.calculate_file_hash()
        super().save(*args, **kwargs)

    def calculate_file_hash(self):
        # Calculate MD5 hash of the file content
        file_hash = hashlib.md5()
        with open(self.path, "rb") as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b""):
                file_hash.update(chunk)
        return file_hash.hexdigest()

    def delete(self, *args, **kwargs):
        # Optionally delete the physical file on deletion of model instance
        # Example: os.remove(self.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name
