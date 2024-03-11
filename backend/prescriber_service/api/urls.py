# prescriber_service/api/urls.py

from django.urls import path
from .views import CSVUploadView, CSVFileStatusView, CSVStatusUpdateView, BlobDownloadView, CSVFileListView

app_name = 'api'  # Django 2.0+ requires you to specify app_name for namespace

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('file-status/<str:csv_file_id>/', CSVFileStatusView.as_view(), name='file-status'),
    path('update-status/<str:csv_file_id>/', CSVStatusUpdateView.as_view(), name='update-status'),
    path('download/<str:blob_name>/', BlobDownloadView.as_view(), name='blob-download'),
    path('files/', CSVFileListView.as_view(), name='file-list'),

]
