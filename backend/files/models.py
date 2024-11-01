import os
import uuid

from django.db import models

from authentication.models import CustomUser
from files.utils import calculate_checksum


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to="uploads/", editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        if os.path.exists(self.file.path):
            os.remove(self.file.path)
        super().delete(*args, **kwargs)


class FileMetadata(models.Model):
    file = models.OneToOneField(
        File,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='metadata'
    )
    file_checksum = models.CharField(
        max_length=50, 
        unique=True, 
        editable=False, 
        null=False, 
        blank=False
    )
    size = models.BigIntegerField(null=False, editable=False)
    file_type = models.CharField(null=False, editable=False)

    def __str__(self):
        return self.file.file.name

    def get_file_checksum(self):
        if self.file is not None:
            self.file_checksum = calculate_checksum(self.file.file)

    def save(self, *args, **kwargs):
        if self.file_checksum is None:
            self.get_file_checksum()
        super().save(*args, **kwargs)