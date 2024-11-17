#files/urls.py
from django.urls import path
from .views import upload_file,download_file

urlpatterns = [
    path('upload/', upload_file, name='file-upload'),
    path('download/<int:file_id>/<str:secure_url>/', download_file, name='file-download'),
]
