from djongo import models

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
