from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
import jwt
from pymongo import MongoClient
from django.conf import settings

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()

                payload = {
                    'username': request.data["username"],
                    'email': request.data["email"],
                    'user_type': "User",
                }

                token = jwt.encode(payload, 'secret_key', algorithm='HS256')

                # decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])

                response = {
                    'message': 'User registered successfully',
                    'token': token
                    }

                return Response(response, status=status.HTTP_201_CREATED)
            return Response({"error": "Ensure input is of right format"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error": "Username has already been used"}, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.password == password:
            payload = {
                'username': username,
                'email': user.email,
                'user_type': "User",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            response = {
                'message': 'User logged in successfully',
                'token': token
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterPrescriber(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        id = request.data.get("provDocID")
        email = request.data.get("email")
        password = request.data.get("password")
        language = request.data.get("language")
        city = request.data.get("city")
        address = request.data.get("address")
        if email is None or password is None or language is None or city is None or address is None or id is None:
            return  Response({"error": "Incorrect request, not all fields sent"}, status=status.HTTP_400_BAD_REQUEST)
        if email == "" or password == "" or language == "" or city == "" or address == "" or id == "":
            return Response({"error": "Not all fields have been filled"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if they've been verified
        client = MongoClient('mongodb+srv://NotParxUsername:NotParxPassword123@atlascluster.fo3q3yw.mongodb.net/')
        db = client['NotParxDB']
        collection = db['api_verified_ids']
        result = collection.find_one({'provDocID': id})

        # Haven't been verified
        if result is None:
            return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)

        collection = db['api_prescriber']
        prescriber = collection.find_one({'provDocID': id})

        if (prescriber is not None) and (prescriber["email"] == "") and (prescriber["password"] == ""):
            # do stuff
            result = collection.update_one(
                {'provDocID': id},
                {'$set': {'email': email, 
                          'password': password, 
                          'language': language,
                          'city': city,
                          'address': address}}
            )

            payload = {
                'provDocID': id,
                'email': email,
                'user_type': "Prescriber",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')

            response = {
                'message': 'Prescriber registered successfully',
                'token': token
                }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'error': 'Already signed up'}, status=status.HTTP_400_BAD_REQUEST)

class LoginPrescriber(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        provDocID = request.data.get('username')
        password = request.data.get('password')
        
        user = Prescriber.objects.filter(provDocID=provDocID).first()
        if user and user.password == password:
            payload = {
                'username': provDocID,
                'email': user.email,
                'user_type': "Prescriber",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            response = {
                'message': 'Prescriber logged in successfully',
                'token': token
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAdmin(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = Admin.objects.filter(username=username).first()
        if user and user.password == password:
            if username == "Coordinator":
                user_type = "Admin - Coordinator"
            else:
                user_type = "Admin - Assistant"

            payload = {
                'username': username,
                'user_type': user_type,
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')

            response = {
                'message': 'User registered successfully',
                'token': token
                }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            response = {
                'message': 'Admin logged in successfully',
                'token': token
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

class GetUserProfiles(APIView):
  permission_classes = [AllowAny]
    
  def get(self, request, format=None):
    if (request.method == 'GET'):
      client = MongoClient(settings.MONGO_URI)
      db = client['NotParxDB']
      collection = db['api_user']
      data = collection.find()


      response = []
      for i in data:
        response.append({
            "username": i.get("username"),
            "password": i.get("password"),
            "firstName": i.get("firstName"),
            "lastName": i.get("lastName"),
            "email": i.get("email"),
            "address": i.get("address"),
            "city": i.get("city"),
            "province": i.get("province"),
            "language": i.get("language"),
            "dpass": i.get("dpass"),
            "actionRequired": i.get("actionRequired"),
            "prescribersID": i.get("prescribersID")
        })
      return JsonResponse(response, safe=False)
    
    return Response({"error": "Error occured"}, status=status.HTTP_400_BAD_REQUEST)
