from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .exceptions import ProfileDoesNotExist
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer


    def retrieve(self, request, username, *args, **kwargs):

        try:

            profile = Profile.objects.select_related('user').get(user=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer
    
    def get_object(self):
        user_id = self.request.user.id
        return Profile.objects.get(user_id= user_id)
    
    def patch(self, request, pk):
        user_id = User.objects.all().get(id =self.request.user.id)
        user = self.request.user
        data = request.data
        
        print('this is the user',request.data)

        serializer = UserProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def profile_detail_api_view(request, username, *args, **kwargs):
#     # get the profile for the passed username
#     qs = Profile.objects.filter(user__username=username)
#     if not qs.exists():
#         return Response({"detail": "User not found"}, status=404)
#     profile_obj = qs.first()
#     data = request.data or {}
#     if request.method == "POST":
#         me = request.user
#         action = data.get("action")
#         if profile_obj.user != me:
#             if action == "follow":
#                 profile_obj.followers.add(me)
#             elif action == "unfollow":
#                 profile_obj.followers.remove(me)
#             else:
#                 pass
    
#     # if request:
#     #     user = request.user
#     #     is_following = FollowerRelationship.objects.filter()
#     #     print('this is_following', is_following)

#     serializer =  ProfileSerializer(instance=profile_obj, context={"request": request})
#     return Response(serializer.data, status=200)
    

