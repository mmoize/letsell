from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import     MessageSerializers, MessagingSerializer, MessagexistSerializer, RoomsSerializer, LobbySerializer, RooomSerializer, MessagexSerializer, RoomxSerializer
from rest_framework.viewsets import ModelViewSet
from discover.models import Post
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Message, Room
from accounts.models import Profile
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from authentication.serializers import UserSerializer
from rest_framework.parsers import JSONParser
from django.http import Http404
from rest_framework import generics, permissions, viewsets

from django.shortcuts import get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from .utils import MultipartJsonParser
from .renderers import JPEGRenderer, PNGRenderer
from rest_framework.exceptions import NotAcceptable





class RoomViewSet( viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RooomSerializer

    def get_queryset(self):
        user = self.request.user
        return user.room_set.all()




class AuthView(object):
    permission_classes = (IsAuthenticated, )


class RoomView(AuthView, APIView):

    def message_tree(self, qs):

        for msg in qs:
            ser = RooomSerializer(msg)
            sender_id = msg.sender.id
            data = ser.data
            newData = {}
            if sender_id == self.request.user.id:
                newData['data'] = ({'msg_data': data, 'sent':True, 'received':False})
            elif sender_id != self.request.user.id:
                newData['data'] = ({'msg_data':data, 'received': True, 'sent':False,})
            print('this is msg', newData)
            #data['children'] = self.message_tree(msg)
            
            yield newData

    def get(self, request,  id, format=None,):
        room = get_object_or_404(Room, pk=1)
        print('hi doon',room)
        page = int(page)
        queryset = Message.objects.filter(room=room ).order_by('-id')
        print('hi doony',self.request.data['id'])
        paginator = Paginator(queryset, 10, allow_empty_first_page=True)
        try:
            roots = paginator.page(page)
        except EmptyPage:
            roots = []
        data = self.message_tree(roots)
        return Response(data)

    def get(self, request, id, page="1", format=None,):
        room = get_object_or_404(Room, pk=int(id))
        print('hi doonx',room)
        page = int(page)
        queryset = Message.objects.filter(room=room).order_by('-id')

        paginator = Paginator(queryset, 10, allow_empty_first_page=True)
        try:
            roots = paginator.page(page)
        except EmptyPage:
            roots = []
        
        print('roots',)
        data = self.message_tree(roots)
        return Response(data)

class LobbyView(AuthView, APIView):
    def populate(self, qs):
        for room in qs:
            ser = LobbySerializer(room)
            data = ser.data
            newest = MessagexSerializer(room.message_set.order_by('-created')[0:1], many=True)
            data['newest'] = newest.data
            yield data

    def get(self, request, format=None):
        result = []
        data = self.populate(Room.objects.filter(members=self.request.user))
        return Response(data)

class MessageView(AuthView, APIView):
    def post(self, request, format=None):
        data = request.data
        print('request-data', data)
        if data.get('id'):
            #no modification of posts allowed
            return 
        ser = MessageySerializer(data=data, partial=True)
        if ser.is_valid():
            ser.object.sender = request.user.id
            ser.save()
            ser.data['children'] = []
        return Response(ser.data)

class MainView(AuthView, APIView):
    def get(self, request, format=None):
        ser = RoomsSerializer(Room.objects.all(), many=True)
        data = ser.data
        print('this is data', data)
        # for i in data:
        #     room_id = i['id']
        #     room = get_object_or_404(Room, pk=room_id)
        #     latest_message = MessagexSerializer(room.message_set.order_by('-created')[0:1], many=True)
        #     i.update( {'latest_message': latest_message})
        #     print('letestmess', i['id'])

        print('serilizer.data', ser.data)
        return Response(data)


class PostMessage(ModelViewSet):
    # Create view for Category objects

    permission_classes = (IsAuthenticated,)  # you are here
    queryset = Message.objects.all()
    serializer_class = MessagexSerializer
    parser_classes = [MultipartJsonParser, JSONParser,]




    def get_serializer_context(self):
        context = super(PostMessage, self).get_serializer_context()
        print('cont', self.request.data)


        if len(self.request.data) > 0:
            context.update({
                'message_info': self.request.data
            })

        return context

    def create(self, request, id, *args, **kwargs):


        # try:
        #     PostImage_serializer = ProductImageSerializer(data=request.FILES)
        #     PostImage_serializer.is_valid(raise_exception=True)
        # except Exception:
        #     raise NotAcceptable(

        #         detail={
        #             'message': 'upload a valid image. The file you uploaded was '
        #                         'neither not an image or a corrupted image.'
        #         }, code=406
        #     )

        serializer = self.get_serializer(data=request.data)


        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print('this is pre-save serializery', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PostMessagexist(ModelViewSet):
    # Create view for Category objects

    permission_classes = (IsAuthenticated,)  # you are here
    queryset = Message.objects.all()
    serializer_class = MessagexistSerializer
    parser_classes = [MultipartJsonParser, JSONParser,]




    def get_serializer_context(self):
        context = super(PostMessagexist, self).get_serializer_context()
        print('cont', self.request.data)


        if len(self.request.data) > 0:
            context.update({
                'message_info': self.request.data
            })

        return context

    def create(self, request, id, *args, **kwargs):


        # try:
        #     PostImage_serializer = ProductImageSerializer(data=request.FILES)
        #     PostImage_serializer.is_valid(raise_exception=True)
        # except Exception:
        #     raise NotAcceptable(

        #         detail={
        #             'message': 'upload a valid image. The file you uploaded was '
        #                         'neither not an image or a corrupted image.'
        #         }, code=406
        #     )

        serializer = self.get_serializer(data=request.data)


        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print('this is pre-save serializery', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)