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
from rest_framework.decorators import api_view, authentication_classes, parser_classes, permission_classes, renderer_classes
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from accounts.models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, ProfileDetailSerializer
from authentication.serializers import UserSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated,])
@renderer_classes([JSONRenderer,])
@parser_classes([FormParser, MultiPartParser])
def detail_api_view(request, username, *args, **kwargs):
    # get the profile for the passed username


    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    other_user = User.objects.get(username=username)
    data = request.data or {}
    if request.method == "POST":
        me = request.user
        current_user_id = request.user.id
        current_user_data = Profile.objects.filter(user__id=current_user_id)
        current_user = current_user_data.first()
        action = data.get("action")
        if profile_obj.user != me:
            if action == "follow":
                profile_obj.followers.add(me)
                current_user.following.add(other_user)
            elif action == "unfollow":
                profile_obj.followers.remove(me)
                current_user.following.remove(other_user)
            else:
                pass
    
    # if request:
    #     user = request.user
    #     is_following = FollowerRelationship.objects.filter()
    #     print('this is_following', is_following)

    serializer =  ProfileSerializer(instance=profile_obj, context={"request": request})

    followed_profile = profile_obj.user.following.all()
    user_following = ProfileSerializer(data=followed_profile, many=True)
    user_following.is_valid()

    followedUsers = {}
    followedUsers.update(serializer.data)

    for item in followed_profile:
        
        followedUsers['following'] = item
        
    
    data = serializer.data
    return JsonResponse(serializer.data, status=200)