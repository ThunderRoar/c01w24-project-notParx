# prescriber_service/api/urls.py

from django.urls import path
from .views import CSVUploadView

app_name = 'api'  # Django 2.0+ requires you to specify app_name for namespace

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
]
