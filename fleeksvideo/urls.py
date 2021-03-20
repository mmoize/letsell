from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import (
    FleekCreateAPIView,
    FleekDeleteAPIView,
    FleekDetailAPIView,
    FleekListAPIView,
    FleekUpdateAPIView,
    CommentCreateAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    fleek_action_view,
    )

app_name = 'fleeksvideo'

urlpatterns = [
    path('', FleekListAPIView.as_view(), name='list'),
    path('create/', FleekCreateAPIView.as_view(), name='create'),
    path('<slug:slug>/', FleekDetailAPIView.as_view(), name='detail'),
    path('edit/<slug:slug>/', FleekUpdateAPIView.as_view(), name='update'),
    path('delete/<slug:slug>/', FleekDeleteAPIView.as_view(), name='delete'),
    path('comments/', CommentListAPIView.as_view(), name='comments_list' ),
    path('comment/create/', CommentCreateAPIView.as_view(), name='comment_create'),
    path('commentdetail/<int:pk>/', CommentDetailAPIView.as_view(), name='comment_thread'),
    path('action', fleek_action_view),
    
]