from pymongo import MongoClient
from django.conf import settings
from bson.objectid import ObjectId
MONGO_URI = settings.MONGO_URI
DATABASE_NAME = "NotParxDB"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
prescription_collection = db["api_prescription"]
user_collection = db["api_user"]
prescriber_collection = db["api_prescriber"]

def get_prescription_by_prescription_id(prescription_id):
    """Retrieve a prescription from MongoDB by its prescriptionID."""
    try:
        return prescription_collection.find_one({'prescriptionID': prescription_id})
    except Exception as e:
        print(e)
        return None
    

def user_details_by_username(username):
    """Retrieve a user from MongoDB by their username."""
    try:
        return user_collection.find_one({'username': username})
    except Exception as e:
        print(e)
        return None
    
def prescriber_details_by_provdocid(prov_doc_id):
    """Retrieve a prescriber from MongoDB by their provDocID."""
    try:
        return prescriber_collection.find_one({'provDocID': prov_doc_id})
    except Exception as e:
        print(e)
        return None