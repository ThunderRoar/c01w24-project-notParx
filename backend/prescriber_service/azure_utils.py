from azure.storage.blob import BlobServiceClient, BlobNotFoundError
from django.conf import settings
# from azure.core.exceptions import BlobNotFoundError

def upload_file_to_blob(file, blob_name):
    """
    Uploads a file to Azure Blob Storage.

    Args:
    file: In-memory file object from the request.FILES.
    blob_name: The name for the blob (file) in Azure Blob Storage.

    Returns:
    The URL to access the uploaded blob.
    """
    # Create a BlobServiceClient object using the connection string.
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    # Get a blob client using the container name and the blob name.
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER_NAME, blob=blob_name)
    # Upload the file to Azure, reading it into memory.
    blob_client.upload_blob(file.read(), overwrite=True)
    # Return the URL to the blob.
    return blob_client.url

def list_blobs_in_container():
    """
    Lists all blobs in the specified Azure Blob Storage container.

    Returns:
    A list of blob names in the container.
    """
    # Create a BlobServiceClient object.
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    # Get a container client to interact with the specified container.
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)
    # List all blobs in the container and return their names.
    return [blob.name for blob in container_client.list_blobs()]

def blob_exists(blob_name):
    """
    Checks if a specific blob exists in the Azure Blob Storage container.

    Args:
    blob_name: The name of the blob to check.

    Returns:
    True if the blob exists, False otherwise.
    """
    # Create a BlobServiceClient object.
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    # Get a blob client for the specific blob.
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER_NAME, blob=blob_name)
    try:
        # Attempt to get blob properties to check existence.
        blob_client.get_blob_properties()
        return True
    except BlobNotFoundError:
        # If the blob is not found, return False.
        return False
    except Exception as e:
        # For any other exceptions, log and handle appropriately.
        print(e)
        return False