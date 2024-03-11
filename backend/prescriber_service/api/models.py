from django.db import models
import uuid

class CSVFile(models.Model):
    """Model to store metadata about uploaded CSV files."""
    csv_file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    current_status = models.CharField(max_length=100, default='In Progress')
    can_download = models.BooleanField(default=False)
    file_location_old = models.CharField(max_length=255, blank=True)
    new_file_location = models.CharField(max_length=255, blank=True) 
    _id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.file_name