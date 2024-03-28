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
    
def get_prescriptions(prescriptionIDs):
    """Retrieve all prescriptions from MongoDB given a list of prescriptionIDs."""
    try:
        match_stage = {
            "$match": {
                "prescriptionID": {"$in": prescriptionIDs}
            }
        }

        # sort prescriptions by date
        date_conversion_stage = {
            "$addFields": {
                "convertedDate": { "$toDate": "$dateOfPrescription" }
            }
        }
        sort_stage = {
            "$sort": { "convertedDate": 1 }
        }

        prescriptions = list(prescription_collection.aggregate([
            match_stage,
            date_conversion_stage,
            sort_stage,
            {"$unset": "convertedDate"} # remove the added field
        ]))

        return prescriptions
    except Exception as e:
        print(e)
        return None

def user_details_by_username(username):
    """Retrieve a user from MongoDB by their username."""
    try:
        # print(f"username: {username}")
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
    
def update_user(username, filters):
    user_collection.update_one({'username': username}, {"$set": filters})

def insert_prescription(prescription):
    prescription_collection.insert_one(prescription)

def update_prescription(prescriptionID, filters):
    prescription_collection.update_one({'prescriptionID': prescriptionID}, {"$set": filters})

def update_prescriber(prescriberID, filters):
    prescriber_collection.update_one({'provDocID': prescriberID}, {"$set": filters})
