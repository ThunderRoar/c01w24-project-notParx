from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from pymongo import MongoClient

# Create a unique provider code for each verified prescriber and upload the provided presciber into the database.
# Parameter: first name, last name, province, college, license number, status
# Return: the unique provider code if verified, else ''
class CreateProviderCode(APIView):
  permission_classes = [AllowAny]

  def post(self, request, format=None):
    try:
      firstName = request.data["firstName"]
      lastName = request.data["lastName"]
      province = request.data["province"]
      college = request.data["college"]
      licenseNum = request.data["licenseNum"]
      presStatus = request.data["status"]
    except KeyError as e:
      return Response({"error": f"Missing required field: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # print("hello" + firstName + lastName + province + college + licenseNum + presStatus)

    try:
      # Connect to MongoDB
      client = MongoClient('mongodb+srv://NotParxUsername:NotParxPassword123@atlascluster.fo3q3yw.mongodb.net/')
      db = client['NotParxDB']
      verifiedIDCollection = db['api_verified_ids']
      presciberCollection = db['api_prescriber']

      # Avoid duplicates uploaded
      result = presciberCollection.find_one({
        "firstName": firstName,
        "lastName": lastName,
        "province": province,
        "licenseNum": licenseNum
      })
      if result is not None:
        return Response({'error': 'Prescriber already recorded'}, status=status.HTTP_400_BAD_REQUEST)

      # Generate unique provider code
      if presStatus == "VERIFIED":
        initials = firstName[0] + lastName[0] if firstName and lastName else ''
        number = 1

        # Check if a prescriber with the same province and initials exists
        pipeline = [
            {"$match": {"province": province, "initials": initials}},
            {"$sort": {"number": -1}},  # in descending order
            {"$limit": 1}
        ]
        result = verifiedIDCollection.aggregate(pipeline)

        if result:
          for doc in result:
            lastNumber = doc['number']
            number = lastNumber + 1

        # Upload new ID
        provDocID = province + '-' + initials + '{:03d}'.format(number)
        document = {
          "provDocID": provDocID,
          "province": province,
          "initials": initials,
          "number": number
        }
        verifiedIDCollection.insert_one(document)

        # Upload prescriber
        document = {
          "firstName": firstName,
          "lastName": lastName,
          "province": province,
          "college": college,
          "licenseNum": licenseNum,
          "status": presStatus,
          "provDocID": provDocID
        }
        presciberCollection.insert_one(document)

        response = {
          'message': 'Prescriber ID created and uploaded successfully',
          'provDocID': provDocID
        }
        return Response(response, status=status.HTTP_201_CREATED)
      else:
        # Upload prescriber
        document = {
          "firstName": firstName,
          "lastName": lastName,
          "province": province,
          "college": college,
          "licenseNum": licenseNum,
          "status": presStatus,
        }
        presciberCollection.insert_one(document)

        response = {
          'message': 'Prescriber uploaded successfully, no ID generated',
          'provDocID': ''
        }
        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
      return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
