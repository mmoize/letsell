
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('join/<int:id>', views.init, name='join'),
]
