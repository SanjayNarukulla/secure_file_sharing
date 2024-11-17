from rest_framework import serializers
from .models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['file_name', 'file', 'uploaded_by', 'upload_date']
