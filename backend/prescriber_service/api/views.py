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
            file_name = file.name
            #file_name = str(uuid.uuid4()) + '.csv'
            
            # Upload the file to Azure Blob Storage
            file_url = upload_file_to_blob(file, file_name)

            # Prepare metadata for MongoDB and Django ORM
            file_metadata = {
                'file_name': file_name,
                'current_status': 'In Progress',
                'can_download': False,
                'file_location_old': file_url,
                # 'file_location_with_status' will be updated after processing
            }

            # Insert file metadata into MongoDB
            insert_csv_file_metadata(file_metadata)

            # Create a Django model instance for the uploaded file
            csv_file = CSVFile(**file_metadata)
            csv_file.save()

            # Serialize the model instance to return as a response
            serializer = CSVFileSerializer(csv_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
