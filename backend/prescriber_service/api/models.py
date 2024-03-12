from djongo import models

class Prescriber(models.Model):
  firstName = models.CharField(max_length=128)
  lastName = models.CharField(max_length=128)
  province = models.CharField(max_length=3)
  college = models.CharField(max_length=128)
  licenseNum = models.CharField(max_length=128)
  status = models.CharField(max_length=128)
  provDocID = models.CharField(max_length=150, unique=True)

class VerifiedPrescriberID(models.Model):
  provDocID = models.CharField(max_length=150, unique=True)
  province = models.CharField(max_length=3)
  initials = models.CharField(max_length=2)
  number = models.IntegerField()
  
  def save(self, *args, **kwargs):
    if not 1 <= self.number <= 999:
        raise ValueError("Number must be 3-digit.")
    return super().save(*args, **kwargs)
