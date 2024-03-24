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
        prescription_data = get_prescription_by_prescription_id(prescription_id)
        print(f"prescription_data: {prescription_data}")
        username= prescription_data.get('patientID') # for the paitent 
        user_data = user_details_by_username(username)
        name = user_data.get('firstName') + ' ' + user_data.get('lastName')

        prov_doc_id = prescription_data.get('prescriberCode')
        prescriber_data = prescriber_details_by_provdocid(prov_doc_id)

        # if prescriber_data or username is None:
        if not prescriber_data or not user_data:
            return HttpResponse('Prescription not found', status=404)
        
        patient_initials = user_data.get('firstName')[0] + user_data.get('lastName')[0]


        activity_plan = prescription_data.get('descriptionOfPrescription', "")

        pdf = create_pdf(
            name=name,
            activity_plan=activity_plan,
            prescriber_code=prov_doc_id,
            patient_initials=patient_initials
        )

        # The PDF data is returned directly, so we create a buffer
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)

        # Return the buffer content as a response
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="prescription.pdf"'
        return response