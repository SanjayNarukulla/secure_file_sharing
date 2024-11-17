from django.db import models
from django.conf import settings

class File(models.Model):
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name
