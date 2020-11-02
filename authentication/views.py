from django.shortcuts import render
from  rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .renderers import UserJSONRenderer
from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import RegistrationSerializer, LoginSerializer, UserFollowingSerializer, UserSerializer
from .models import UserFollowing, User

class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):

        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        #user_data = request.data.get('user', {})
        user_data = request.data
        print(user_data)
        serializer_data = {
            'username': user_data.get('username', request.user.username),
            #'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),

            'profile': {
                'first_name': user_data.get('first_name', request.user.profile.first_name),
                'last_name': user_data.get('last_name', request.user.profile.last_name),
                'country': user_data.get('country', request.user.profile.country),
                'city' : user_data.get('city', request.user.profile.city),
                'bio': user_data.get('bio', request.user.profile.bio),
                'image': user_data.get('image', request.user.profile.image),
            }
        }

        serializer = self.serializer_class(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginApIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserFollowingViewSet(ModelViewSet):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = UserFollowingSerializer
    queryset = UserFollowing.objects.all()


    def get_queryset(self): 
        user = User.objects.get(id=self.request.user.id) # it is just example with id 1   
        user.following.all()
        user.followers.all()

        userfollowing = {}
        userfollowing['following'] = user.following.all()
        userfollowing['follower'] = user.followers.all()

        return userfollowing



    def create(self, request, id, *args, **kwargs):
        followingUser_obj = User.objects.get(id=id)
        userFollowing_obj = UserFollowing.objects.create(user=self.request.user, following=followingUser_obj)
        print('this is the userfollowing_ob', userFollowing_obj)

        user = User.objects.get(id=self.request.user.id) # it is just example with id 1
        user.following.all()
        user.followers.all()
        print('this is anotherone', user.followers.all())
        # user.following.all()
        # user.followers.all()

        # print('this is anotherone', user.following.all())

        # following_data = UserFollowingSerializer(userFollowing_obj.following.all(), many=True)
        # followers_data = UserFollowingSerializer(userFollowing_obj.followers.all(), many=True)
        return JsonResponse({'status':status.HTTP_200_OK, 'data':{'user':user.following.all(), 'following':user.following.all(), 'followers':followers_data.data}, "message":"success"})

