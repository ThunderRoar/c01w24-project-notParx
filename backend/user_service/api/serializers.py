from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'firstName', 'lastName', 'email', 'address', 'city', 'province', 'language', 'dpass', 'actionRequired', 'prescriptionIDs']

class PrescriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriber
        fields = ['provDocID', 'password'] # removed id field