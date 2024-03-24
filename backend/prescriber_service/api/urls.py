from django.urls import path
from . import views



app_name = 'api'  # Django 2.0+ requires you to specify app_name for namespace

urlpatterns = [
    path('upload/', views.CSVUploadView.as_view(), name='csv-upload'),
    path('file-status/<str:csv_file_id>/', views.CSVFileStatusView.as_view(), name='file-status'),
    path('download/<str:csv_file_id>/', views.BlobDownloadView.as_view(), name='blob-download'),
    path('files/', views.CSVFileListView.as_view(), name='file-list'),
    path('update-status/', views.CSVStatusUpdateView.as_view(), name='update-csv-status'),
    path('createID/', views.CreateProviderCode.as_view(), name='createID'),
  path('getPrescriberProfiles/', views.GetPrescriberProfiles.as_view(), name='getPrescriberProfiles')
]
