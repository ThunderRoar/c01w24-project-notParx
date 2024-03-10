from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'firstName', 'lastName', 'address', 'dpass', 'actionRequired', 'perscribersID']

class PerscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perscriber
        fields = ['provDocID', 'password'] # removed id field