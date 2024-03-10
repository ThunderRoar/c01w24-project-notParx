from django.urls import path
from . import views

urlpatterns = [
	path('registerUser/', views.RegisterUser.as_view(), name='registerUser'),
	path('loginUser/', views.LoginUser.as_view(), name='loginUser'),
    path('registerPerscriber/', views.RegisterPerscriber.as_view(), name='registerPerscriber'),
    path('loginPerscriber/', views.LoginPerscriber.as_view(), name='loginPerscriber'),
	path('loginAdmin/', views.LoginAdmin.as_view(), name='loginAdmin'),
]