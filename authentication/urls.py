from django.urls import path
from .views import RegistrationAPIView, UserRetrieveUpdateAPIView, UserFollowingViewSet, LoginApIView
from rest_framework import routers


app_name = 'authentication'

userFollwingLink = UserFollowingViewSet.as_view({'post': 'create'})
getuserFollwingLink = UserFollowingViewSet.as_view({'get': 'list'})


urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="user"),
    path('users/', RegistrationAPIView.as_view(), name="user_registration"),
    path('users/login/', LoginApIView.as_view(), name="user_login"),
    path('userfollowinglink/<int:id>', userFollwingLink, name='postdetail'),
    path('getuserfollowinglink', getuserFollwingLink, name='postdetail')
]
