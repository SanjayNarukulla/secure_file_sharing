import hashlib
import base64
import time
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import File
from django.core.exceptions import ObjectDoesNotExist

# Helper function to generate a secure URL with expiration time
def generate_secure_url(file_id, user, expiration_time=3600):  # Default expiration is 1 hour
    # Generate a timestamp for expiration (current time + expiration time)
    expiration_timestamp = int(time.mktime(timezone.now().timetuple())) + expiration_time
    # Generate a secure hash based on file_id, user email, and expiration timestamp
    data = f"{file_id}-{user.email}-{expiration_timestamp}"
    secure_hash = hashlib.sha256(data.encode()).hexdigest()
    return urlsafe_base64_encode(secure_hash.encode())

# Helper function to verify the secure URL
def verify_secure_url(file_id, secure_url, user):
    # Decode the secure URL and get the hash
    try:
        decoded_hash = urlsafe_base64_decode(secure_url).decode()
    except Exception:
        return False

    # Recreate the expected hash with an expiration timestamp
    expiration_timestamp = int(time.mktime(timezone.now().timetuple()))
    expected_hash = generate_secure_url(file_id, user, expiration_time=expiration_timestamp)

    if decoded_hash != expected_hash:
        return False

    # Check if the link is expired
    expiration_timestamp = int(time.mktime(timezone.now().timetuple()))
    if expiration_timestamp < int(time.mktime(timezone.now().timetuple())):
        return False
    
    return True

# API view to handle file upload
@api_view(['POST'])
def upload_file(request):
    # Check if file is in request
    if 'file' not in request.FILES:
        return Response({'message': 'No file provided'}, status=400)

    # Handle file upload
    file = request.FILES['file']
    new_file = File.objects.create(file=file, uploaded_at=timezone.now())
    return Response({'message': 'File uploaded successfully', 'file_id': new_file.id}, status=201)

# API view to handle file download
@api_view(['GET'])
def download_file(request, file_id, secure_url):
    try:
        file = File.objects.get(id=file_id)
    except File.DoesNotExist:
        return Response({'message': 'File not found'}, status=404)

    # Check if the user is a client
    if request.user.user_type != 'client':
        return Response({'message': 'Unauthorized'}, status=403)

    # Verify the secure URL and expiration
    if not verify_secure_url(file_id, secure_url, request.user):
        return Response({'message': 'Invalid or expired download link'}, status=400)

    # Return the file URL for download
    file_url = file.file.url  # Django will serve the file if MEDIA_URL is configured
    return Response({'file_url': file_url, 'message': 'success'})
