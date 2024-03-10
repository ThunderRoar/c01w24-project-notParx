from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
import jwt

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
        practitioner = Practitioner.objects.filter(username=username).first()
        admin = Admin.objects.filter(username=username).first()
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
        elif practitioner and practitioner.password == password:
            payload = {
                'username': username,
                'user_type': "Practitioner",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            response = {
                'message': 'Practitioner logged in successfully',
                'token': token
                }
            return Response(response, status=status.HTTP_200_OK)
        elif admin and admin.password == password:
            payload = {
                'username': username,
                'user_type': "Admin",
            }

            token = jwt.encode(payload, 'secret_key', algorithm='HS256')
            response = {
                'message': 'Admin logged in successfully',
                'token': token
                }
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
