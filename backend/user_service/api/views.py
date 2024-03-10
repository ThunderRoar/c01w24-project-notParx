from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
import jwt
from pymongo import MongoClient

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            payload = {
                'username': request.data["username"],
                'user_type': "User",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')

            # decoded_token = jwt.decode(token, 'secret_key', algorithms=['HS256'])

            response = {
                'message': 'User registered successfully',
                'token': token
                }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        if user and user.password == password:
            payload = {
                'username': username,
                'user_type': "User",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            response = {
                'message': 'User logged in successfully',
                'token': token
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

class RegisterPerscriber(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        id = request.data["provDocID"]

        # Check if they've been verified
        client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.5')
        db = client['test_db']
        collection = db['VerifiedIDs']
        result = collection.find_one({'provDocID': id})

        # Haven't been verified
        if result is None:
            return Response({'error': 'Invalid ID'}, status=status.HTTP_400_BAD_REQUEST)

        collection = db['api_perscriber']

        perscriber = collection.find_one({'provDocID': id})
        if (perscriber is not None) and (perscriber["email"] == "") and (perscriber["password"] == ""):
            # do stuff
            email = request.data["email"]
            password = request.data["password"]
            result = collection.update_one(
                {'provDocID': id},
                {'$set': {'email': email, 'password': password}}
            )

            payload = {
                'provDocID': id,
                'user_type': "Perscriber",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')

            response = {
                'message': 'Perscriber registered successfully',
                'token': token
                }

            return Response(response, status=status.HTTP_201_CREATED)
        return Response({'error': 'Invalid ID or already signed up'}, status=status.HTTP_400_BAD_REQUEST)

class LoginPerscriber(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        provDocID = request.data.get('username')
        password = request.data.get('password')
        
        user = Perscriber.objects.filter(provDocID=provDocID).first()
        if user and user.password == password:
            payload = {
                'username': provDocID,
                'user_type': "Perscriber",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            response = {
                'message': 'Perscriber logged in successfully',
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
