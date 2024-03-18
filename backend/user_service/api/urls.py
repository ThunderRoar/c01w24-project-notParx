from django.urls import path
from . import views

urlpatterns = [
	path('registerUser/', views.RegisterUser.as_view(), name='registerUser'),
	path('loginUser/', views.LoginUser.as_view(), name='loginUser'),
    path('registerPrescriber/', views.RegisterPrescriber.as_view(), name='registerPrescriber'),
    path('loginPrescriber/', views.LoginPrescriber.as_view(), name='loginPrescriber'),
	path('loginAdmin/', views.LoginAdmin.as_view(), name='loginAdmin'),
    path('getUserProfiles/',views.GetUserProfiles.as_view(), name='getUserProfiles'),
]