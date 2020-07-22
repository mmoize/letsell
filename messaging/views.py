from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import MessageSerializers
from rest_framework.viewsets import ModelViewSet
from discover.models import Post
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Message
from accounts.models import Profile
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
# Create your views here.


class MessageCreateView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializers

    def get_serializer_context(self):
        context = super( MessageCreateView, self).get_serializer_context()
        recipient = User.objects.filter(username=self.kwargs['username'])
        print('this is req', recipient)

        if len(self.request.data) > 0:
            context.update({
                'included_images': self.request.FILES
            })
            
            print('this is for the included_images', context['included_images'])             
        return context
        
    def create(self,request, *args, **kwargs):
        sender_user_query = User.objects.filter(id=self.request.user.id)
        sender_user_id = sender_user_query.get(id=self.request.user.id)
        sender = sender_user_id.id

        user_query = User.objects.filter(username=self.kwargs['username'])
        user_recipient = user_query.get(username=self.kwargs['username'])
        recipient = user_recipient.id

        print('this is req', recipient)

        reque = {}
        ref_post_query = Post.objects.filter(id=self.request.data['referenced_post']).order_by('-updated_at')
        ref_post_id = ref_post_query.get(id=self.request.data['referenced_post'])
        post = ref_post_id.id
        print('this is ', post)
        body = self.request.data['body']
        ref_post =self.request.data['referenced_post']
        subject = self.request.data['subject']
        
        reque.update({'body': body})
        reque.update({'sender': sender})
        reque.update({'subject': subject})
        reque.update({'recipient': recipient})
        reque.update({'referenced_post': ref_post})
        print('this is req', reque)
        serializer = MessageSerializers(data=reque)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headerss = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headerss)


class MessageDetailView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializers
    #queryset = Message.objects.all()
    def get_serializer_context(self):
        context = super( MessageDetailView, self).get_serializer_context()
        message = Message.objects.get(id=self.request.data['id'])

        if message.recipient == self.request.user.id:
            context['in_inbox'] = True
            context['social_in'] = Profile.objects.get(user_id=message.sender)
            context['thread'] = Message.objects.filter(sender=message.sender, recipient=message.sender).order_by("-created")
        else:
            context['in_inbox'] = False
            context['social_in'] = Profile.objects.get(user_id=message.recipient)
            context['thread'] = Message.objects.filter(sender=message.recipient, recipient=message.recipient).order_by("-created")
          
        return context


class MessagelistView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializers

    def get_queryset(self):
        data_ =  self.request.data
        _referenced_post = data_['referenced_post']
        _recipient = data_['recipient']
        print('this is request', data_)
        messages = Message.objects.filter(referenced_post=_referenced_post, recipient=_recipient,  sender=self.request.user).order_by("-created")

        return messages

    # def get_queryset(self):
    #     context = super(  MessagelistView, self).get_queryset()
    #     context['outbox'] = Message.objects.filter(sender=self.request.user.id).order_by('-created')  
    #     context['inbox'] = Message.objects.filter(recipient=self.request.user.id).order_by('-created')        
    #     return context

# class MessagelistView(ModelViewSet):
#     queryset = Message.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = MessageSerializers


#     def  get(self, request, format=None):


#         print('ths is queryset', queryset)



#         serializer = MessageSerializers(queryset)  
#         serializer.is_valid()   
#         return Response(serializer.data)


class InboxView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializers
    queryset = Message.objects.all()

    def get(self, request, format=None):
        context = {}
        context['outbox'] = Message.objects.filter(sender=self.request.user.id).order_by('-created')  
        context['inbox'] = Message.objects.filter(recipient=self.request.user.id).order_by('-created')
        data_outbox = list(context['outbox'])
        data_inbox = list(context['inbox'])
        print('outbox', data_outbox)
        print('inbox', len(data_inbox))
        cont_outbox = {}
        re_cont = []

        for i in data_outbox:
             message_id = i.id
             id = i.sender.id
             re_id = i.recipient.id
             p_id = i.referenced_post.id
             created_at = i.created
             cont_outbox.update({
                 'sender': id,
                 'recipient': re_id,
                 'subject': i.subject,
                 'referenced_post': p_id,
                 'body': i.body,
                 'message_id': message_id,
             })
             serializer = MessageSerializers(data=cont_outbox)
             serializer.is_valid()
             re_cont.append({'outbox': serializer.data, 'id': message_id, 'created':created_at})
   
             cont_outbox = {}

        cont_inbox = {}
        for i in data_inbox:
             message_id = i.id
             print('this is message_id', message_id)
             id = i.sender.id
             re_id = i.recipient.id
             p_id = i.referenced_post.id
             created_at = i.created
             cont_inbox.update({
                 'sender': id,
                 'recipient': re_id,
                 'subject': i.subject,
                 'referenced_post': p_id,
                 'body': i.body,
                 'message_id': message_id,
             })
             serializer = MessageSerializers(data=cont_inbox)
             serializer.is_valid()
             re_cont.append({'inbox': serializer.data, 'id': message_id, 'created':created_at})
             cont = {}
        

        print('this is re_cont', context['inbox'])
        return Response(re_cont)
# You ARE HERE.....................................................