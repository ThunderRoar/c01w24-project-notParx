from pymongo import MongoClient
from bson.objectid import ObjectId  # Important for handling MongoDB's default _id field
import os

uri = 'mongodb+srv://NotParxUsername:NotParxPassword123@atlascluster.fo3q3yw.mongodb.net/'
# MONGO_URI = os.environ.get("MONGO_URI")
MONGO_URI = uri
DATABASE_NAME = "CSV_DB"

client = MongoClient(uri)
db = client[DATABASE_NAME]
csv_files_collection = db["CSV_collections"]

def insert_csv_file_metadata(document):
    """Insert a new document into the MongoDB collection."""
    print(document)  # For debugging, consider using proper logging in production
    return csv_files_collection.insert_one(document).inserted_id

def get_csv_metadata_by_id(csv_file_id):
    """Retrieve a document from MongoDB by its _id."""
    try:
        # Ensure _id is treated as an ObjectId for querying
        return csv_files_collection.find_one({'_id': ObjectId(csv_file_id)})
    except Exception as e:
        print(e)  # For debugging, consider using proper logging in production
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
