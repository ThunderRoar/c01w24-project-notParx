from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from io import BytesIO

from PDF_generation import create_pdf
from mongo_utils import get_prescription_by_prescription_id, user_details_by_username, prescriber_details_by_provdocid

class DownloadPrescriptionPDF(APIView):
    """
    API endpoint to download a prescription PDF.
    """
    permission_classes = [AllowAny]

    def get(self, request, prescription_id, format=None):
        """
        Get the prescription data and create a PDF.
        """      
        # Using the funciont get_prescription_by_id from mongo_utils.py
        prescription_data = get_prescription_by_id(prescription_id)
        
        user_data = user_details(prescription_data.get('user_id'))
        name = user_data.get('firstName') + ' ' + user_data.get('lastName')
        activity_plan = prescription_data.get('DescriptionOfPrescription')
        presriber_code = prescription_data.get('PrescriberCode')
        patient_initials = user_data.get('firstName')[0] + user_data.get('lastName')[0]
        pdf = create_pdf(
            name=name,
            activity_plan=activity_plan,
            prescription_code=presriber_code,
            patient_initials=patient_initials
        )

        # The PDF data is returned directly, so we create a buffer
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        # Return the buffer content as a response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="prescription.pdf"'