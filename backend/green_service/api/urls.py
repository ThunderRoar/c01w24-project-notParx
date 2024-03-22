from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('map/', views.MapView.as_view(), name='map-view'),
]