from django.contrib.auth.decorators import login_required
from rest_framework.parsers import FileUploadParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status

from files.serializers import FileSerializer
from files.models import File

@login_required
@api_view(["POST"])
@parser_classes([FileUploadParser])
def upload_file(request):
    raw_file = request.data['file']
    file_data = {
        'file': raw_file,
        'user': request.user,
    }
    serializer = FileSerializer(data=file_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(["GET"])
def get_files(request):
    files = File.objects.all().order_by("-uploaded_at")
    files_serializer = FileSerializer(files, many=True)
    return Response(files_serializer.data, status=status.HTTP_200_OK)
    

@login_required
@api_view(["DELETE"])
def delete_file(request, pk):
    try:
        file = File.objects.get(user=request.user, pk=pk)
    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    file.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
