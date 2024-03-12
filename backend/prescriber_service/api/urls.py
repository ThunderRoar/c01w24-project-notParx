from django.urls import path
from . import views

urlpatterns = [
  path('createID/', views.CreateProviderCode.as_view(), name='createID'),
]