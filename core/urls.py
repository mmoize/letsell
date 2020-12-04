from django.urls import path

from .views import  detail_api_view


app_name = 'core'



urlpatterns = [
    path('<str:username>/', detail_api_view),
    path('<str:username>/follow', detail_api_view),

]
