from rest_framework import serializers
from .models import *

class PrescriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriber
        fields = ['firstName', 'lastName', 'province', 'college', 'licenseNum', 'status', 'provDocID']

class VerifiedPrescriberIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedPrescriberID
        fields = ['provDocID', 'province', 'initials', 'number']
