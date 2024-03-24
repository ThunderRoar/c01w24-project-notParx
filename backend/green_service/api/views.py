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
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')

# Create your views here.
