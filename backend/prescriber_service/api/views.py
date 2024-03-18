from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import *
from .serializers import *
from pymongo import MongoClient
import datetime
from .models import CSVFile
from .serializers import CSVFileSerializer
from azure_utils import upload_file_to_blob, blob_exists, list_blobs_in_container, get_blob_download_url
from mongo_utils import insert_csv_file_metadata, update_csv_status, get_csv_status_by_id, get_all_csv_metadata, get_csv_metadata_by_new_file_name, get_csv_metadata_by_old_file_name, get_csv_metadata_by_id
import uuid
from django.conf import settings
import requests
import threading


# Create a unique provider code for each verified prescriber and upload them into the database.
# Parameter: first name, last name, province, college, license number, status
# Return: the unique provider code if verified
class CreateProviderCode(APIView):
  permission_classes = [AllowAny]

  def post(self, request, format=None):
    try:
      firstName = request.data["firstName"]
      lastName = request.data["lastName"]
      province = request.data["province"]
      college = request.data["college"]
      licenseNum = request.data["licenseNum"]
      presStatus = request.data["status"]
    except KeyError as e:
      return Response({"error": f"Missing required field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
      # Connect to MongoDB
      client = MongoClient(settings.MONGO_URI)
      db = client['NotParxDB']
      verifiedIDCollection = db['api_verified_ids']
      presciberCollection = db['api_prescriber']

      # Avoid duplicates uploaded
      result = presciberCollection.find_one({
        "firstName": firstName,
        "lastName": lastName,
        "province": province,
        "licenseNum": licenseNum
      })
      if result is not None:
        return Response({'error': 'Prescriber already recorded'}, status=status.HTTP_400_BAD_REQUEST)

      # Generate unique provider code
      if presStatus == "VERIFIED":
        initials = firstName[0] + lastName[0] if firstName and lastName else ''
        number = 1

        # Check if a prescriber with the same province and initials exists
        pipeline = [
            {"$match": {"province": province, "initials": initials}},
            {"$sort": {"number": -1}},  # in descending order
            {"$limit": 1}
        ]
        result = verifiedIDCollection.aggregate(pipeline)

        if result:
          for doc in result:
            lastNumber = doc['number']
            number = lastNumber + 1

        # Upload new ID
        provDocID = province + '-' + initials + '{:03d}'.format(number)
        document = {
          "provDocID": provDocID,
          "province": province,
          "initials": initials,
          "number": number
        }
        verifiedIDCollection.insert_one(document)

        # Upload prescriber
        document = {
          "firstName": firstName,
          "lastName": lastName,
          "email": '',
          "province": province,
          "college": college,
          "licenseNum": licenseNum,
          "status": presStatus,
          "password": '',
          "provDocID": provDocID,
          "prescriptions": [],
          "language": '',
          "city": '',
          "address": ''
        }
        presciberCollection.insert_one(document)

        response = {
          'message': 'Prescriber ID created and uploaded successfully',
          'provDocID': provDocID
        }
        return Response(response, status=status.HTTP_201_CREATED)
      else:
        return Response({'error': 'Prescriber not verified'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class CSVUploadView(APIView):
    permission_classes = [AllowAny]

    """API view to handle CSV file uploads."""
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if file:
            unique_file_name = str(uuid.uuid4()) + '.csv'  # Generate a unique file name for Azure
            upload_file_to_blob(file, unique_file_name)  # Upload to Azure Blob Storage

            # Prepare metadata
            file_metadata = {
                'file_name': file.name,
                'date_uploaded': datetime.datetime.now(),
                'current_status': 'In Progress',
                'file_location_old': unique_file_name,  # Original file name
                'new_file_location': "",  # Will be updated later (processed file name)
            }

            # Insert file metadata into MongoDB
            mongo_db_id = insert_csv_file_metadata(file_metadata)

            # Trigger the Azure function asynchronously
            self.initiate_verification_process(unique_file_name)

            # Prepare response
            # serializer = CSVFileSerializer(csv_file)
            # response_data = serializer.data
            # response_data['mongo_id'] = str(mongo_db_id)  # Include MongoDB ID in the response
            # return Response(response_data, status=status.HTTP_201_CREATED)
            return Response({"mongoid":str(mongo_db_id)}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    def initiate_verification_process(self, csv_name):
        """Starts an asynchronous GET request to trigger the verification process."""
        def verify_csv():
            encoded_csv_name = requests.utils.quote(csv_name)
            url = f'https://c01notparx-verifer.azurewebsites.net/api/verifier?csv_name={encoded_csv_name}'
            try:
                requests.get(url, timeout=10)
            except requests.RequestException as e:
                print(f"Error initiating verification for {csv_name}: {e}")

        # Start the GET request in a new thread
        thread = threading.Thread(target=verify_csv)
        thread.start()



class CSVStatusUpdateView(APIView):
    permission_classes = [AllowAny]

    """
    API view to update the status of an uploaded CSV file based on the processing outcome.
    Expects JSON data containing 'old_file_name' and 'status'.
    'status' should be either 'processed' or 'not processed'.
    If 'processed', 'new_file_name' is expected.
    """
    def post(self, request, format=None):
        old_file_name = request.data.get('old_file_name')
        process_status = request.data.get('status')
        new_file_name = request.data.get('new_file_name', '')  # Default to empty string if not provided

        if not old_file_name or not process_status:
            return Response({'error': 'Missing data.'}, status=status.HTTP_400_BAD_REQUEST)

        if process_status not in ['processed', 'not processed']:
            return Response({'error': 'Invalid status provided.'}, status=status.HTTP_400_BAD_REQUEST)

        csv_metadata = get_csv_metadata_by_old_file_name(old_file_name)
        if not csv_metadata:
            return Response({'error': 'CSV file not found.'}, status=status.HTTP_404_NOT_FOUND)

        if process_status == 'processed':
            if not new_file_name or not blob_exists(new_file_name):
                return Response({'error': 'New file does not exist in Azure Blob Storage.'}, status=status.HTTP_404_NOT_FOUND)

            # If processed successfully, update the document with the new file location and status 'Uploaded'
            update_result = update_csv_status(
                csv_metadata['_id'],
                'Uploaded',
                new_file_location=new_file_name
            )
        else:
            # If not processed, update the document status to 'Failed'
            update_result = update_csv_status(
                csv_metadata['_id'],
                'Failed'
            )

        if update_result:
            return Response({'status': 'Update successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Update failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CSVFileStatusView(APIView):
    permission_classes = [AllowAny]

    """
    API view to check the status of a CSV file stored in MongoDB using MongoDB's _id.
    """
    def get(self, request, csv_file_id, format=None):
        status = get_csv_status_by_id(csv_file_id)
        if status:
            return Response({'status': status}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'File not found or failed to retrieve status.'}, status=status.HTTP_404_NOT_FOUND)
        

class BlobDownloadView(APIView):
    permission_classes = [AllowAny]

    """
    API view to download a file stored in Azure Blob Storage.
    Expects MongoDB _id to determine the correct file to download.
    """
    def get(self, request, csv_file_id, format=None):
        # Retrieve the file metadata from MongoDB using its _id
        csv_metadata = get_csv_metadata_by_id(csv_file_id)
        if not csv_metadata:
            return Response({'error': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Determine which file to download: new file if available and exists, otherwise old file
        blob_name_to_download = csv_metadata.get('new_file_location') if csv_metadata.get('new_file_location') and blob_exists(csv_metadata.get('new_file_location')) else csv_metadata.get('file_location_old')
        
        # Generate a download URL for the determined blob
        download_url = get_blob_download_url(blob_name_to_download)

        if download_url:
            return Response({'download_url': download_url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to generate download URL.'}, status=status.HTTP_404_NOT_FOUND)
        

class CSVFileListView(APIView):
    permission_classes = [AllowAny]

    """
    API view to list all CSV files stored.
    """
    def get(self, request, format=None):
        csv_metadata_list = get_all_csv_metadata()
        # Convert MongoDB documents to a format suitable for JSON response
        # MongoDB's _id field needs to be converted to string
        for doc in csv_metadata_list:
            doc['_id'] = str(doc['_id'])
        
        return Response(csv_metadata_list, status=status.HTTP_200_OK)