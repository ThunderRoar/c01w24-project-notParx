from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from io import BytesIO

from PDF_generation import create_pdf
from mongo_utils import (
    get_prescription_by_prescription_id,
    user_details_by_username,
    prescriber_details_by_provdocid,
    update_user, insert_prescription,
    update_prescription,
    update_prescriber,
    get_prescriptions )

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
        if activity_plan == None:
            activity_plan = ""

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
        response['Content-Disposition'] = f'attachment; filename="PaRx - {prov_doc_id}.pdf"'
        return response 
    
class LogUserPrescription(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # Get prescription info
        date = request.data.get("date")
        prescriberID = request.data.get("prescriberID")
        discoveryPass = request.data.get("discoveryPass")
        username = request.data.get("username")
        description = request.data.get("description")

        # Make unique string

        # Add prescription to list of prescriptions if not already there
        user = user_details_by_username(username=username)
        prescriber = prescriber_details_by_provdocid(prov_doc_id=prescriberID)
        if prescriber is None:
            return Response({'error': 'No prescriber with that ID'}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            firstName = user["firstName"].upper()
            lastName = user["lastName"].upper()
            initials = "" + firstName[0] + lastName[0]

            prescriptionString = prescriberID + "_" + date + "_" + initials

            prescriptions = user['prescriptionIDs']
            for prescription in prescriptions:
                if prescription == prescriptionString:
                    return Response({'error': 'Prescription already logged'}, status=status.HTTP_400_BAD_REQUEST)

            prescriptions.append(prescriptionString)

            filters = {'prescriptionIDs': prescriptions}
            update_user(username=username, filters=filters)

            # Check for existing prescription and update status accordingly
            existingPrescription = get_prescription_by_prescription_id(prescription_id=prescriptionString)
            if existingPrescription is None:
                newPrescription = {
                    'prescriptionID': prescriptionString,
                    'patientID': username,
                    'matched': False,
                    'prescriberCode': prescriberID,
                    'dateOfPrescription': date,
                    'descriptionOfPrescription': description,
                    'discoveryPassPrescribed': discoveryPass,
                    'patientStatus': "Pr not logged yet",
                    'prescriberStatus': ""
                }
                insert_prescription(prescription=newPrescription)
            else:
                if discoveryPass:
                    if user["address"] == "DNE":
                        update_user(username=username, filters={'actionRequired': True})
                    filters = {'matched': True, 'patientStatus': 'Pr logged', 'prescriberStatus': 'Pa logged', 'patientID': username}
                else:
                    filters = {'matched': True, 'patientStatus': 'Complete', 'prescriberStatus': 'Complete', 'patientID': username}
                update_prescription(prescriptionID=prescriptionString, filters=filters)
            
            return Response({'success': 'Added prescription'}, status=status.HTTP_200_OK)

        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

class LogPrescriberPrescription(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        # Get prescription info
        initials = request.data.get("initials")
        date = request.data.get("date")
        prescriberID = request.data.get("prescriberID")
        discoveryPass = request.data.get("discoveryPass")
        description = request.data.get("description")

        # Make unique string

        prescriptionString = prescriberID + "_" + date + "_" + initials

        # Add prescription to list of prescriptions if not already there
        prescriber = prescriber_details_by_provdocid(prescriberID)
        if prescriber:
            prescriptions = prescriber['prescriptions']
            for prescription in prescriptions:
                if prescription == prescriptionString:
                    return Response({'error': 'Prescription already logged'}, status=status.HTTP_400_BAD_REQUEST)

            prescriptions.append(prescriptionString)

            filters = {'prescriptions': prescriptions}
            update_prescriber(prescriberID=prescriberID, filters=filters)

            # Check for existing prescription and update status accordingly
            existingPrescription = get_prescription_by_prescription_id(prescription_id=prescriptionString)
            if existingPrescription is None:
                newPrescription = {
                    'prescriptionID': prescriptionString,
                    'patientID': "",
                    'matched': False,
                    'prescriberCode': prescriberID,
                    'dateOfPrescription': date,
                    'descriptionOfPrescription': description,
                    'discoveryPassPrescribed': discoveryPass,
                    'patientStatus': "",
                    'prescriberStatus': "Pa not logged yet"
                }

                insert_prescription(prescription=newPrescription)
            else:
                if discoveryPass:
                    username = existingPrescription["patientID"]
                    user = user_details_by_username(username=username)
                    if user and user["address"] == "DNE" :
                        update_user(username=username, filters={'actionRequired': True})
                    filters = {'matched': True, 'patientStatus': 'Pr logged', 'prescriberStatus': 'Pa logged'}
                else:
                    filters = {'matched': True, 'patientStatus': 'Complete', 'prescriberStatus': 'Complete'}
                update_prescription(prescriptionID=prescriptionString, filters=filters)
            
            return Response({'success': 'Added prescription'}, status=status.HTTP_200_OK)

        return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

# Pull prescriptions based on prescriberCode (ie: provDocID)
class GetPrescriberPrescriptions(APIView):
    permission_classes = [AllowAny]

    def get(self, request, prescriber_code, format=None):
        prescriber_profile = prescriber_details_by_provdocid(prescriber_code)

        if prescriber_profile:
            prescription_ids = prescriber_profile.get("prescriptions")
            prescriptions = get_prescriptions(prescription_ids)

            if prescriptions or prescriptions == []:
                # Add patient names for each prescription
                for prescription in prescriptions:
                    username = prescription.get('patientID')
                    user_data = user_details_by_username(username)
                    
                    if user_data != None:
                        prescription['matchedPatient'] = user_data.get('firstName') + ' ' + user_data.get('lastName')
                    else:
                        prescription['matchedPatient'] = "N/A"

                    # Convert MongoDB documents to a format suitable for JSON response
                    # MongoDB's _id field needs to be converted to string
                    prescription['_id'] = str(prescription['_id'])

                return Response(prescriptions)
            else: # prescriptions == None
                return Response({'error': 'Something went wrong when retrieving prescriptions'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error: Prescriber not found'}, status=status.HTTP_400_BAD_REQUEST)

# Pull prescriptions based on patientID (ie: patient's username)
class GetPatientPrescriptions(APIView):
    permission_classes = [AllowAny]

    def get(self, request, patient_id, format=None):
        patient_profile = user_details_by_username(patient_id)

        if patient_profile:
            prescription_ids = patient_profile.get("prescriptionIDs")
            prescriptions = get_prescriptions(prescription_ids)

            if prescriptions or prescriptions == []:
                # Remove other patients with the same initials
                prescriptions = [p for p in prescriptions if p.get('patientID') == patient_id]

                # Convert MongoDB documents to a format suitable for JSON response
                # MongoDB's _id field needs to be converted to string
                for doc in prescriptions:
                    doc['_id'] = str(doc['_id'])

                return Response(prescriptions)
            else: # prescriptions == None
                return Response({'error': 'Something went wrong when retrieving prescriptions'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error: Patient not found'}, status=status.HTTP_400_BAD_REQUEST)

class UpdatePrescription(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, prescription_id, format=None):
        try:
            prescription = get_prescription_by_prescription_id(prescription_id)

            if not prescription:
                return Response({'error': 'Prescription not found'}, status=status.HTTP_404_NOT_FOUND)

            new_status = request.data.get("status")
            if new_status:
                prescription['prescriberStatus'] = new_status

            # Add logic for other fields

            update_prescription(prescriptionID=prescription_id, filters=prescription)

            return Response({'message': 'Prescription updated'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
