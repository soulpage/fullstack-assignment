from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import CustomUser
from chat.models import Conversation, UploadedFile


class SummaryAndUploadApiTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user("files@example.com", "password", is_active=True)
        self.other_user = CustomUser.objects.create_user("other@example.com", "password", is_active=True)
        self.client.force_login(self.user)

    def test_summaries_are_paginated_and_filterable(self):
        Conversation.objects.create(user=self.user, title="Python notes", summary="Django pagination")
        Conversation.objects.create(user=self.user, title="Travel", summary="Packing list")
        Conversation.objects.create(user=self.other_user, title="Private", summary="Do not return")

        response = self.client.get(reverse("get_conversation_summaries"), {"search": "django", "page_size": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Python notes")

    @override_settings(MEDIA_ROOT="/tmp/chat-upload-tests")
    def test_upload_list_duplicate_and_delete(self):
        upload_url = reverse("uploaded_files")
        file_data = b"identical file contents"

        response = self.client.post(
            upload_url,
            {"file": SimpleUploadedFile("notes.txt", file_data, content_type="text/plain")},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        uploaded_id = response.data["id"]
        self.assertEqual(response.data["original_name"], "notes.txt")
        self.assertEqual(response.data["size"], len(file_data))

        duplicate = self.client.post(
            upload_url,
            {"file": SimpleUploadedFile("renamed.txt", file_data, content_type="text/plain")},
            format="multipart",
        )
        self.assertEqual(duplicate.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(self.client.get(upload_url).data[0]["id"], uploaded_id)

        self.assertTrue(UploadedFile.objects.filter(pk=uploaded_id).exists())
        deleted = self.client.delete(reverse("delete_uploaded_file", kwargs={"pk": uploaded_id}))
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UploadedFile.objects.filter(pk=uploaded_id).exists())

    def test_file_cannot_be_deleted_by_another_user(self):
        uploaded = UploadedFile.objects.create(
            user=self.other_user,
            file="",
            original_name="private.txt",
            size=7,
            sha256="a" * 64,
        )

        response = self.client.delete(reverse("delete_uploaded_file", kwargs={"pk": uploaded.id}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(UploadedFile.objects.filter(pk=uploaded.id).exists())
