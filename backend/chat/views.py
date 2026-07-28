import hashlib

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from chat.models import Conversation, Message, UploadedFile, Version
from chat.serializers import (
    ConversationSerializer,
    ConversationSummaryFilterSerializer,
    ConversationSummarySerializer,
    MessageSerializer,
    TitleSerializer,
    UploadedFileSerializer,
    VersionSerializer,
)
from chat.utils.branching import make_branched_conversation


@api_view(["GET"])
def chat_root_view(request):
    return Response({"message": "Chat works!"}, status=status.HTTP_200_OK)


@login_required
@api_view(["GET"])
def get_conversations(request):
    conversations = Conversation.objects.filter(user=request.user, deleted_at__isnull=True).order_by("-modified_at")
    serializer = ConversationSerializer(conversations, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ConversationSummaryPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


@login_required
@api_view(["GET"])
def get_conversation_summaries(request):
    """Return the current user's non-deleted conversation summaries."""
    filters = ConversationSummaryFilterSerializer(data=request.query_params)
    filters.is_valid(raise_exception=True)

    conversations = Conversation.objects.filter(user=request.user, deleted_at__isnull=True).order_by("-modified_at")
    data = filters.validated_data
    if search := data.get("search"):
        conversations = conversations.filter(Q(title__icontains=search) | Q(summary__icontains=search))
    if title := data.get("title"):
        conversations = conversations.filter(title__icontains=title)
    if created_after := data.get("created_after"):
        conversations = conversations.filter(created_at__gte=created_after)
    if created_before := data.get("created_before"):
        conversations = conversations.filter(created_at__lte=created_before)

    paginator = ConversationSummaryPagination()
    page = paginator.paginate_queryset(conversations, request)
    serializer = ConversationSummarySerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


def get_upload_sha256(upload):
    digest = hashlib.sha256()
    for chunk in upload.chunks():
        digest.update(chunk)
    upload.seek(0)
    return digest.hexdigest()


@login_required
@api_view(["GET", "POST"])
def uploaded_files(request):
    if request.method == "GET":
        files = UploadedFile.objects.filter(user=request.user)
        return Response(UploadedFileSerializer(files, many=True, context={"request": request}).data)

    upload = request.FILES.get("file")
    if upload is None:
        return Response({"file": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    checksum = get_upload_sha256(upload)
    if UploadedFile.objects.filter(user=request.user, sha256=checksum).exists():
        return Response({"detail": "This file has already been uploaded."}, status=status.HTTP_409_CONFLICT)

    uploaded_file = UploadedFile(
        user=request.user,
        file=upload,
        original_name=upload.name,
        content_type=upload.content_type or "",
        size=upload.size,
        sha256=checksum,
    )
    try:
        with transaction.atomic():
            uploaded_file.save()
    except IntegrityError:
        # The database constraint also covers simultaneous uploads of identical content.
        # Saving a FileField happens before the database insert, so clean that blob up.
        uploaded_file.file.delete(save=False)
        return Response({"detail": "This file has already been uploaded."}, status=status.HTTP_409_CONFLICT)

    return Response(
        UploadedFileSerializer(uploaded_file, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
    )


@login_required
@api_view(["DELETE"])
def delete_uploaded_file(request, pk):
    try:
        uploaded_file = UploadedFile.objects.get(pk=pk, user=request.user)
    except UploadedFile.DoesNotExist:
        return Response({"detail": "Uploaded file not found."}, status=status.HTTP_404_NOT_FOUND)

    # FileField does not remove the stored object when its model row is deleted.
    uploaded_file.file.delete(save=False)
    uploaded_file.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
@api_view(["GET"])
def get_conversations_branched(request):
    conversations = Conversation.objects.filter(user=request.user, deleted_at__isnull=True).order_by("-modified_at")
    conversations_serializer = ConversationSerializer(conversations, many=True)
    conversations_data = conversations_serializer.data

    for conversation_data in conversations_data:
        make_branched_conversation(conversation_data)

    return Response(conversations_data, status=status.HTTP_200_OK)


@login_required
@api_view(["GET"])
def get_conversation_branched(request, pk):
    try:
        conversation = Conversation.objects.get(user=request.user, pk=pk)
    except Conversation.DoesNotExist:
        return Response({"detail": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)

    conversation_serializer = ConversationSerializer(conversation)
    conversation_data = conversation_serializer.data
    make_branched_conversation(conversation_data)

    return Response(conversation_data, status=status.HTTP_200_OK)


@login_required
@api_view(["POST"])
def add_conversation(request):
    try:
        conversation_data = {"title": request.data.get("title", "Mock title"), "user": request.user}
        conversation = Conversation.objects.create(**conversation_data)
        version = Version.objects.create(conversation=conversation)

        messages_data = request.data.get("messages", [])
        for idx, message_data in enumerate(messages_data):
            message_serializer = MessageSerializer(data=message_data)
            if message_serializer.is_valid():
                message_serializer.save(version=version)
                if idx == 0:
                    version.save()
            else:
                return Response(message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        conversation.active_version = version
        conversation.save()
        conversation.refresh_summary()

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(["GET", "PUT", "DELETE"])
def conversation_manage(request, pk):
    try:
        conversation = Conversation.objects.get(user=request.user, pk=pk)
    except Conversation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ConversationSerializer(conversation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
@api_view(["PUT"])
def conversation_change_title(request, pk):
    try:
        conversation = Conversation.objects.get(user=request.user, pk=pk)
    except Conversation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TitleSerializer(data=request.data)

    if serializer.is_valid():
        conversation.title = serializer.data.get("title")
        conversation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({"detail": "Title not provided"}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(["PUT"])
def conversation_soft_delete(request, pk):
    try:
        conversation = Conversation.objects.get(user=request.user, pk=pk)
    except Conversation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    conversation.deleted_at = timezone.now()
    conversation.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
@api_view(["POST"])
def conversation_add_message(request, pk):
    try:
        conversation = Conversation.objects.get(user=request.user, pk=pk)
        version = conversation.active_version
    except Conversation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if version is None:
        return Response({"detail": "Active version not set for this conversation."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(version=version)
        conversation.refresh_summary()
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": serializer.data,
                "conversation_id": conversation.id,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(["POST"])
def conversation_add_version(request, pk):
    try:
        conversation = Conversation.objects.get(user=request.user, pk=pk)
        version = conversation.active_version
        root_message_id = request.data.get("root_message_id")
        root_message = Message.objects.get(pk=root_message_id)
    except Conversation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Message.DoesNotExist:
        return Response({"detail": "Root message not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if root message belongs to the same conversation
    if root_message.version.conversation != conversation:
        return Response({"detail": "Root message not part of the conversation"}, status=status.HTTP_400_BAD_REQUEST)

    new_version = Version.objects.create(
        conversation=conversation, parent_version=root_message.version, root_message=root_message
    )

    # Copy messages before root_message to new_version
    messages_before_root = Message.objects.filter(version=version, created_at__lt=root_message.created_at)
    new_messages = [
        Message(content=message.content, role=message.role, version=new_version) for message in messages_before_root
    ]
    Message.objects.bulk_create(new_messages)

    # Set the new version as the current version
    conversation.active_version = new_version
    conversation.save()
    conversation.refresh_summary()

    serializer = VersionSerializer(new_version)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
@api_view(["PUT"])
def conversation_switch_version(request, pk, version_id):
    try:
        conversation = Conversation.objects.get(pk=pk)
        version = Version.objects.get(pk=version_id, conversation=conversation)
    except Conversation.DoesNotExist:
        return Response({"detail": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
    except Version.DoesNotExist:
        return Response({"detail": "Version not found"}, status=status.HTTP_404_NOT_FOUND)

    conversation.active_version = version
    conversation.save()
    conversation.refresh_summary()

    return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
@api_view(["POST"])
def version_add_message(request, pk):
    try:
        version = Version.objects.get(pk=pk)
    except Version.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MessageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(version=version)
        version.conversation.refresh_summary()
        return Response(
            {
                "message": serializer.data,
                "version_id": version.id,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
