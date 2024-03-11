import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CSVFile
from .serializers import CSVFileSerializer
from azure_utils import upload_file_to_blob, blob_exists, list_blobs_in_container
from mongo_utils import insert_csv_file_metadata, get_csv_metadata_by_id, update_csv_status
import uuid


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
                'date_uploaded': datetime.now(),
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
    """API view to update the status of an uploaded CSV file."""
    def post(self, request, csv_file_id, format=None):
        csv_metadata = get_csv_metadata_by_id(csv_file_id)
        if not csv_metadata:
            return Response({'error': 'CSV file not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Use new_file_location to check if the file exists in Azure Blob Storage
        if blob_exists(csv_metadata['new_file_location']):
            update_csv_status(csv_file_id, 'Uploaded')
            return Response({'status': 'Uploaded'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Not uploaded'}, status=status.HTTP_404_NOT_FOUND)
