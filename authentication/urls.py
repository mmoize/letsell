from django.urls import path
from .views import RegistrationAPIView, UserRetrieveUpdateAPIView, LoginApIView
from rest_framework import routers


app_name = 'authentication'


urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="user"),
    path('users/', RegistrationAPIView.as_view(), name="user_registration"),
    path('users/login/', LoginApIView.as_view(), name="user_login"),
]
