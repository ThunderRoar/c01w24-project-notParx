from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view

from io import BytesIO

from PDF_generation import create_pdf
from mongo_utils import get_prescription_by_id, user_details

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
        prescription_data = request.query_params

        # Using the funciont get_prescription_by_id from mongo
        prescription_id = prescription_data.get('prescription_id')
        
        # Using the funciont get_prescription_by_id from mongo_utils.py
        prescription_data = get_prescription_by_id(prescription_id)
        
        user_data = user_details(prescription_data.get('user_id'))
        name = user_data.get('firstName') + ' ' + user_data.get('lastName')
        activity_plan = prescription_data.get('DescriptionOfPrescription')
        prescription_code = prescription_data.get('prescription_code')
        # Create a PDF and return it as a response
        pdf = create_pdf(
            name=prescription_data.get('name', 'Default Name'),
            activity_plan=prescription_data.get('activity_plan', 'Default Activity Plan'),
            prescription_code=prescription_data.get('prescription_code', 'Default Code'),
            patient_initials=prescription_data.get('patient_initials', 'Default Initials'),
            user_name=user_data.get('name', 'Default User Name'),
            user_email=user_data.get('email', 'Default User Email')
        )
        
        pdf = create_pdf(
            name=prescription_data.get('name', 'Default Name'),
            activity_plan=prescription_data.get('activity_plan', 'Default Activity Plan'),
            prescription_code=prescription_data.get('prescription_code', 'Default Code'),
            patient_initials=prescription_data.get('patient_initials', 'Default Initials')
        )

        # The PDF data is returned directly, so we create a buffer
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        # Return the buffer content as a response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="prescription.pdf"'