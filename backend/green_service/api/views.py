from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
import datetime
import requests
import os
from arcgis.gis import GIS
from dotenv import load_dotenv

load_dotenv()
ARCGIS_KEY=os.getenv('ARCGIS_KEY')

# # Create your views here.
# class MapView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, format=None):
#         if request.method == "GET":




#             # # Check if the request was successful
#             # if response.status_code == 200:
#             #     data = response.json()
#             # else:
#             #     return Response(response.text, status=status.HTTP_400_BAD_REQUEST)

#             return JsonResponse(data, safe=False)
