# azure_utils.py

from azure.storage.blob import BlobServiceClient
from django.conf import settings

def upload_file_to_blob(file, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER_NAME, blob=blob_name)

    blob_client.upload_blob(file.read(), overwrite=True)
    return blob_client.url  # Returns the URL to access the blob

def list_blobs_in_container():
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)
    
    return [blob.name for blob in container_client.list_blobs()]

def blob_exists(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER_NAME, blob=blob_name)
    try:
        blob_client.get_blob_properties()
        return True
    except Exception as e:
        return False