from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from pymongo import MongoClient
import datetime
from .models import CSVFile
from .serializers import CSVFileSerializer
from azure_utils import upload_file_to_blob, blob_exists, list_blobs_in_container, get_blob_download_url
from mongo_utils import insert_csv_file_metadata, update_csv_status, get_csv_status_by_id, get_all_csv_metadata, get_csv_metadata_by_new_file_name
import uuid

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
      client = MongoClient('settings.MONGO_URI')
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
                'can_download': False,
                'file_location_old': file.name,  # Original file name
                'new_file_location': unique_file_name,  # Azure Blob Storage unique file name
            }

            # Insert file metadata into MongoDB
            mongo_db_id = insert_csv_file_metadata(file_metadata)

            # Optionally, create a Django model instance
            csv_file = CSVFile(**file_metadata)
            csv_file.save()

            # Prepare response
            serializer = CSVFileSerializer(csv_file)
            response_data = serializer.data
            response_data['mongo_id'] = str(mongo_db_id)  # Include MongoDB ID in the response

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

class CSVStatusUpdateView(APIView):
    """
    API view to update the status of an uploaded CSV file.
    This view expects a unique Azure Blob Storage file name (new_file_name),
    not the MongoDB _id.
    """
    def post(self, request, new_file_name, format=None):
        # Find the CSV metadata by the new_file_name
        csv_metadata = get_csv_metadata_by_new_file_name(new_file_name)
        if not csv_metadata:
            return Response({'error': 'CSV file not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the file exists in Azure Blob Storage
        if blob_exists(new_file_name):
            # Update the status in MongoDB if the file exists
            # Use the MongoDB _id to update the status
            update_csv_status(csv_metadata['_id'], 'Uploaded')
            return Response({'status': 'Uploaded'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Not uploaded'}, status=status.HTTP_404_NOT_FOUND)


class CSVFileStatusView(APIView):
    """
    API view to check the status of a CSV file stored in MongoDB.
    """
    def get(self, request, csv_file_id, format=None):
        status = get_csv_status_by_id(csv_file_id)
        if status:
            return Response({'status': status}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'File not found or failed to retrieve status.'}, status=status.HTTP_404_NOT_FOUND)
        

class BlobDownloadView(APIView):
    """
    API view to get the download URL of a file stored in Azure Blob Storage.
    """
    def get(self, request, blob_name, format=None):
        download_url = get_blob_download_url(blob_name)
        if download_url:
            return Response({'download_url': download_url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to generate download URL.'}, status=status.HTTP_404_NOT_FOUND)
        

class CSVFileListView(APIView):
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