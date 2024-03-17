from rest_framework import serializers
from .models import *

class PrescriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescriber
        fields = ['firstName',
                  'lastName',
                  'email',
                  'province',
                  'college',
                  'licenseNum',
                  'status',
                  'password',
                  'provDocID',
                  'prescriptions',
                  'language',
                  'city',
                  'address']

class VerifiedPrescriberIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifiedPrescriberID
        fields = ['provDocID', 'province', 'initials', 'number']

class CSVFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = '__all__'
