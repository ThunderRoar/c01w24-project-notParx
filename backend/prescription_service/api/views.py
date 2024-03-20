from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from PDF_generation import create_pdf

class DownloadPrescriptionPDF(APIView):
    """
    API endpoint to download a prescription PDF.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Get the prescription data and create a PDF.
        """
        # Get the prescription data from the request
        prescription_data = JSONParser().parse(request)

        # Create the PDF
        create_pdf(
            name=prescription_data['name'],
            activity_plan=prescription_data['activity_plan'],
            prescription_code=prescription_data['prescription_code'],
            patient_initials=prescription_data['patient_initials']
        )

        # Return the response
        return JsonResponse({'message': 'PDF created successfully.'}, status=status.HTTP_200_OK)