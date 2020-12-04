from django.urls import path

from .views import ProfileRetrieveAPIView, profile_detail_api_view


app_name = 'profiles'



urlpatterns = [
    path('profiles/<str:username>/', ProfileRetrieveAPIView.as_view()),
    path('<str:username>/', profile_detail_api_view),
    path('<str:username>/follow', profile_detail_api_view),

]
