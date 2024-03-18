from django.urls import path
from . import views
from .views import CSVUploadView, CSVFileStatusView, CSVStatusUpdateView, BlobDownloadView, CSVFileListView


app_name = 'api'  # Django 2.0+ requires you to specify app_name for namespace

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('file-status/<str:csv_file_id>/', CSVFileStatusView.as_view(), name='file-status'),
    path('download/<str:csv_file_id>/', BlobDownloadView.as_view(), name='blob-download'),
    path('files/', CSVFileListView.as_view(), name='file-list'),
    path('update-status/', CSVStatusUpdateView.as_view(), name='update-csv-status'),
    path('createID/', views.CreateProviderCode.as_view(), name='createID'),
]
