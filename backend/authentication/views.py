from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view

from authentication.models import CustomUser
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Conversation, FileUpload
from .serializers import ConversationSerializer, FileUploadSerializer
from .permissions import IsAdminOrReadOnly
import logging
from django.core.cache import cache
from rest_framework.response import Response

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'all_conversations'
        cached_data = cache.get(cache_key)
        if cached_data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=60*15)  # Cache for 15 minutes
            return Response(response.data)
        return Response(cached_data)


logger = logging.getLogger(__name__)

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        logger.info(f'File uploaded by {request.user} with filename {response.data["file"]}')
        return response

    def destroy(self, request, *args, **kwargs):
        file = self.get_object()
        logger.info(f'File deleted by {request.user} with filename {file.file.name}')
        return super().destroy(request, *args, **kwargs)

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        # Your file upload logic
        return super().create(request, *args, **kwargs)

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

class FileUploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if file:
            # Handle file duplication and other custom logic here
            # For example, check if a file with the same name already exists
            if FileUpload.objects.filter(file=file.name).exists():
                return Response({'error': 'File with this name already exists'}, status=400)
        return super().create(request, *args, **kwargs)


@api_view(["GET"])
def auth_root_view(request):
    return JsonResponse({"message": "Auth endpoint works!"})


@api_view(["GET"])
def csrf_token(request):
    token = get_token(request)
    return JsonResponse({"data": token})


@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    # Check if the user is active
    if not user.is_active:
        return JsonResponse({"error": "User is not active"}, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        response = JsonResponse({"data": "Login successful"})

        # Set session cookie manually
        session_key = request.session.session_key
        session_cookie_name = settings.SESSION_COOKIE_NAME
        max_age = settings.SESSION_COOKIE_AGE
        response.set_cookie(session_cookie_name, session_key, max_age=max_age, httponly=True)

        return response
    else:
        return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def logout_view(request):
    logout(request)
    response = JsonResponse({"data": "Logout successful"})
    response.delete_cookie(settings.SESSION_COOKIE_NAME)

    return response


@api_view(["POST"])
def register_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return JsonResponse({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email is already taken"}, status=status.HTTP_400_BAD_REQUEST)

    CustomUser.objects.create_user(email, password=password)
    return JsonResponse({"data": "User created successfully"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def verify_session(request):
    session_cookie = request.COOKIES.get("sessionid")
    is_authenticated = request.user.is_authenticated and session_cookie == request.session.session_key
    return JsonResponse({"data": is_authenticated})
