from pymongo import MongoClient
import os

uri = 'mongodb+srv://NotParxUsername:<password>@atlascluster.fo3q3yw.mongodb.net/?retryWrites=true&w=majority'
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
