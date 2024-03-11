from pymongo import MongoClient
import os

uri = 'mongodb+srv://NotParxUsername:NotParxPassword123@atlascluster.fo3q3yw.mongodb.net/'
# MONGO_URI = os.environ.get("MONGO_URI")
MONGO_URI = uri
DATABASE_NAME = "CSV_DB"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

csv_files_collection = db["CSV_collections"]

# Function to insert document into a collection
def insert_csv_file_metadata(document):
    collection = csv_files_collection
    print(document)
    return collection.insert_one(document).inserted_id
