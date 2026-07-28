# Generated manually for the uploaded-file API.

import uuid

import django.db.models.deletion
import chat.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_conversation_summary"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("file", models.FileField(upload_to=chat.models.uploaded_file_path)),
                ("original_name", models.CharField(max_length=255)),
                ("content_type", models.CharField(blank=True, max_length=255)),
                ("size", models.PositiveBigIntegerField()),
                ("sha256", models.CharField(max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="uploaded_files",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(
            model_name="uploadedfile",
            constraint=models.UniqueConstraint(fields=("user", "sha256"), name="unique_uploaded_file_hash_per_user"),
        ),
    ]
