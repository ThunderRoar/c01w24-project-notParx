from pymongo import MongoClient
from bson.objectid import ObjectId  # Important for handling MongoDB's default _id field
from django.conf import settings
import os

# MONGO_URI = os.environ.get("MONGO_URI")
MONGO_URI = settings.MONGO_URI
DATABASE_NAME = "CSV_DB"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
csv_files_collection = db["CSV_collections"]

def insert_csv_file_metadata(document):
    """Insert a new document into the MongoDB collection."""
    print(document)  # For debugging, consider using proper logging in production
    return csv_files_collection.insert_one(document).inserted_id


def get_csv_metadata_by_new_file_name(new_file_name):
    """Retrieve a document from MongoDB by the new file name used in Azure Blob Storage."""
    try:
        return csv_files_collection.find_one({'new_file_location': new_file_name})
    except Exception as e:
        print(e)
        return None


def update_csv_status(csv_file_id, status, can_download=None, new_file_location=None):
    """Update the status and potentially other fields of a document in MongoDB."""
    update_fields = {'current_status': status}
    if can_download is not None:
        update_fields['can_download'] = can_download
    if new_file_location:
        update_fields['new_file_location'] = new_file_location
    
    try:
        csv_files_collection.update_one(
            {'_id': ObjectId(csv_file_id)},  # Ensure _id is treated as an ObjectId
            {'$set': update_fields}
        )
        return True
    except Exception as e:
        print(e)  # For debugging, consider using proper logging in production
        return False

def get_csv_status_by_id(csv_file_id):
    """Retrieve the status of a CSV file from MongoDB by its _id."""
    try:
        document = csv_files_collection.find_one({'_id': ObjectId(csv_file_id)}, {'current_status': 1, '_id': 0})
        return document['current_status'] if document else None
    except Exception as e:
        print(e)  # Log error for debugging
        return None
    

def get_all_csv_metadata():
    """Retrieve all CSV file metadata documents from MongoDB."""
    try:
        documents = csv_files_collection.find({})
        return list(documents)
    except Exception as e:
        print(e)  # Log error for debugging
        return []
    
def get_csv_metadata_by_old_file_name(old_file_name):
    """Retrieve a document from MongoDB by the old file name."""
    try:
        return csv_files_collection.find_one({'file_location_old': old_file_name})
    except Exception as e:
        print(e)
        return None
    
def get_csv_metadata_by_id(csv_file_id):
    """
    Retrieve a document from MongoDB using its _id.
    
    Args:
    csv_file_id (str): The string representation of the MongoDB ObjectId.
    
    Returns:
    dict: The document corresponding to the _id, or None if not found.
    """
    try:
        # Convert the string ID to ObjectId
        document = csv_files_collection.find_one({'_id': ObjectId(csv_file_id)})
        return document
    except Exception as e:
        print(f"Error retrieving document by _id: {e}")
        return None