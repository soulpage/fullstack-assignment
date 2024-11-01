from rest_framework import serializers

from authentication.models import CustomUser
from files.models import File, FileMetadata
from files.utils import calculate_checksum


class FileMetadataSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileMetadata
        fields = [
            'file_checksum',
            'size',
            'file_type',
        ]


class FileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="email", queryset=CustomUser.objects.all())
    metadata = FileMetadataSerializer(required=False)

    class Meta:
        model = File
        fields = [
            'id', 
            'file',
            'metadata',
            'user',
            'uploaded_at'
        ]

    def validate(self, data):
        file = data['file']
        file_checksum = calculate_checksum(file)

        data['metadata'] = {
            'file_checksum': file_checksum,
            'size': file.size,
            'file_type': file.content_type,
        }

        if FileMetadata.objects.filter(file_checksum=file_checksum).exists():
            raise serializers.ValidationError("This file already exists.")

        return data

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        file = File.objects.create(**validated_data)
        FileMetadata.objects.create(file=file, **metadata_data)
        return file