from djongo import models

class User(models.Model):
    username = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    dpass = models.BooleanField(default=False)
    actionRequired = models.BooleanField(default=False)
    perscribersID = models.JSONField(default=list)

    def __str__(self):
        return self.username

class Perscriber(models.Model):
    provDocID = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username
