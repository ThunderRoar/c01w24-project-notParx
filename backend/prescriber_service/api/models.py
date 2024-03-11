from django.db import models
import uuid

class CSVFile(models.Model):
    csv_file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    current_status = models.CharField(max_length=100, default='In Progress')  # e.g., 'Complete', 'In Progress'
    can_download = models.BooleanField(default=False)
    file_location_old = models.CharField(max_length=255, blank=True)  # File location on Azure before processing
    file_location_with_status = models.CharField(max_length=255, blank=True)  # File location on Azure after processing

    def __str__(self):
        return self.file_name
