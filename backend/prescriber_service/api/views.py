from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CSVFile
from .serializers import CSVFileSerializer
from azure_utils import upload_file_to_blob
from mongo_utils import insert_csv_file_metadata
import uuid

class CSVUploadView(APIView):

    def post(self, request, format=None):
        file = request.FILES.get('file')
        if file:
            # Generate a unique file name
            file_name = str(uuid.uuid4()) + '.csv'
            
            # Upload the file to Azure Blob Storage
            file_url = upload_file_to_blob(file, file_name)

            # Prepare metadata for MongoDB
            file_metadata = {
                'file_name': file_name,
                'current_status': 'In Progress',
                'can_download': False,
                'file_location_old': file_url,
                # 'file_location_with_status' will be updated after processing
            }

            # Insert file metadata into MongoDB
            mongo_db_id = insert_csv_file_metadata(file_metadata)

            # Create a Django model instance for the uploaded file, excluding MongoDB-specific fields
            csv_file = CSVFile(
                file_name=file.name,
                current_status='In Progress',
                can_download=False,
                file_location_old=file_url,
            )
            csv_file.save()

            # Add the MongoDB id to the response data manually
            serializer = CSVFileSerializer(csv_file)
            response_data = serializer.data
            response_data['mongo_id'] = str(mongo_db_id)  # Convert ObjectId to string for JSON serialization

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
