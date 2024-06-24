from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Conversation
from .serializers import ConversationSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    pagination_class = PageNumberPagination  # Optional: for pagination

    def get_queryset(self):
        queryset = Conversation.objects.all()
        # Implement filtering logic based on query parameters
        return queryset


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UploadedFile
from .serializers import UploadedFileSerializer
from rest_framework.pagination import PageNumberPagination


class FileUploadView(APIView):
    def post(self, request, format=None):
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            # Check if the file already exists
            existing_file = UploadedFile.objects.filter(file__exact=request.data['file'])
            if existing_file.exists():
                return Response({'error': 'File already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FileListView(APIView):
    def get(self, request, format=None):
        files = UploadedFile.objects.all()
        serializer = UploadedFileSerializer(files, many=True)
        return Response(serializer.data)

class FileDeleteView(APIView):
    def delete(self, request, file_id, format=None):
        try:
            file_to_delete = UploadedFile.objects.get(id=file_id)
        except UploadedFile.DoesNotExist:
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        file_to_delete.file.delete(save=False)  # Delete file from storage
        file_to_delete.delete()  # Delete file record from database
        return Response({'message': 'File deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
