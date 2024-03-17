from djongo import models
from django.db import models
import uuid

class Prescriber(models.Model):
  firstName = models.CharField(max_length=128)
  lastName = models.CharField(max_length=128)
  email = models.CharField(max_length=128)
  province = models.CharField(max_length=3)
  college = models.CharField(max_length=128)
  licenseNum = models.CharField(max_length=128)
  status = models.CharField(max_length=128)
  password = models.CharField(max_length=128)
  provDocID = models.CharField(max_length=150, unique=True)
  prescriptions = models.JSONField(default=list)
  language = models.CharField(max_length=128)
  city = models.CharField(max_length=128)
  address = models.CharField(max_length=128)

class VerifiedPrescriberID(models.Model):
  provDocID = models.CharField(max_length=150, unique=True)
  province = models.CharField(max_length=3)
  initials = models.CharField(max_length=2)
  number = models.IntegerField()
  
  def save(self, *args, **kwargs):
    if not 1 <= self.number <= 999:
        raise ValueError("Number must be 3-digit.")
    return super().save(*args, **kwargs)


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