from django.urls import path
from . import views



app_name = 'api'  # Django 2.0+ requires you to specify app_name for namespace

urlpatterns = [
    path('downloadprescription/<str:prescription_id>/', views.DownloadPrescriptionPDF.as_view(), name='download-prescription'), # Self generated prescription id
    path('logUserPrescription/', views.LogUserPrescription.as_view(), name='logUserPrescription'),
    path('logPrescriberPrescription/', views.LogPrescriberPrescription.as_view(), name='logPrescriberPrescription'),
]
