# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt

# from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from .serializers import     MessageSerializers, MessagingSerializer, MessagexistSerializer, RoomsSerializer, LobbySerializer, RooomSerializer, MessagexSerializer, RoomxSerializer
# from rest_framework.viewsets import ModelViewSet
# from discover.models import Post
# from rest_framework.response import Response
# from rest_framework import status, generics
# from .models import Message, Room
# from accounts.models import Profile
# from rest_framework.views import APIView
# from django.http import HttpResponse, JsonResponse
# from authentication.serializers import UserSerializer
# from rest_framework.parsers import JSONParser
# from django.http import Http404
# from rest_framework import generics, permissions, viewsets

# from django.shortcuts import get_list_or_404, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage
# from .utils import MultipartJsonParser
# from .renderers import JPEGRenderer, PNGRenderer
# from rest_framework.exceptions import NotAcceptable


import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from stream_chat import StreamChat

from .models import Member
from authentication.models import User


# @csrf_exempt
# def init(request):
#     if not request.body:
#         return JsonResponse(status=200, data={'message': 'No request body'})
#     body = json.loads(bytes(request.body).decode('utf-8'))

#     if 'username' not in body:
#         return JsonResponse(status=400, data={'message': 'Username is required to join the channel'})



@csrf_exempt
def init(request, id):
    ...

    client = StreamChat(api_key=settings.STREAM_API_KEY,api_secret=settings.STREAM_API_SECRET)
                        
    channel = client.channel('messaging', 'General')

    try:
        member = Member.objects.get(user=id)
        token = client.create_token(user_id=id)
        print('this is the token ', token)
        #token = bytes(client.create_token(user_id=id)).encode('utf-8')
        return JsonResponse(status=200, data={"username": member.user.username, "token": token, "apiKey": settings.STREAM_API_KEY})

    except Member.DoesNotExist:
        user_instance = User.objects.get(id=id) 
        member = Member(user=user_instance)
        member.save()
        token = bytes(client.create_token(user_id=id)).decode('utf-8')
        client.update_user({"id": id, "role": "admin"})
        channel.add_members([])

        return JsonResponse(status=200, data={"username": user_instance.username, "token": token, "apiKey": settings.STREAM_API_KEY})




