  
import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.parsers import JSONParser
from .utils import  MultipartJsonParser
from rest_framework.exceptions import NotAcceptable
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import Fleek, FleeksImage
from accounts.models import Profile
from .serializers import (
    FleekSerializer, 
    FleekActionSerializer,
    FleekCreateSerializer,
    FleekImageSerializer,
    Fleek_ImageSerializer
)

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


class FleekCreateView(viewsets.ModelViewSet):
    # Create view for Category objects
    permission_classes = (IsAuthenticated,)  
    queryset = Fleek.objects.all()
    serializer_class = FleekSerializer
    parser_classes = [MultipartJsonParser, JSONParser,]


    cont = None

    def get_serializer_context(self):
        context = super(FleekCreateView, self).get_serializer_context()
 
        if len(self.request.data) > 0:
            context.update({
                'included_images': self.request.FILES
            })

            context.update({
                'fleeks_info': self.request.data
            })

        print('context', context)
        cont = context
        return context

    def create(self, request, *args, **kwargs):

        try:
            FleekImage_serializer = FleekImageSerializer(data=request.FILES)
            FleekImage_serializer.is_valid(raise_exception=True)
           

        
        except Exception:
            
            raise NotAcceptable(
                detail={
                    'message': 'upload a valid image. The file you uploaded was '
                                'neither not an image or a corrupted image.'
                }, code=406
            )
    
        serializer = self.get_serializer(data=request.data)
        
        
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])

@permission_classes([IsAuthenticated])
def fleek_create_view(request, *args, **kwargs):
    serializer = FleekCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        profile = Profile.objects.get(user=request.user)
        serializer.save(user=profile)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@csrf_exempt
@permission_classes([IsAuthenticated])
def GetFleekDetail(request, id):

    if request.method == 'GET':

        fleek = Fleek.objects.filter(id=id)
        serializer = FleekSerializer(fleek, many=True)
        return JsonResponse(serializer.data, safe=False)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fleek_detail_view(request, fleek_id, *args, **kwargs):
    qs = Fleek.objects.filter(id=fleek_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = FleekSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def fleek_delete_view(request, fleek_id, *args, **kwargs):
    qs = Fleek.objects.filter(id=fleek_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this fleek"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "fleek removed"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fleek_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike, retweet
    '''
    serializer = FleekActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        fleek_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
        qs = Fleek.objects.filter(id=fleek_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            user_profile = Profile.objects.get(user=request.user)
            obj.likes.add(user_profile)
            serializer = FleekSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            user_profile = Profile.objects.get(user=request.user)
            obj.likes.remove(user_profile)
            serializer = FleekSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet":
            user_profile = Profile.objects.get(user=request.user)
            new_fleek = Fleek.objects.create(
                    user=user_profile, 
                    parent=obj,
                    content=content,
                    )
            serializer = FleekSerializer(new_fleek)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


def get_paginated_queryset_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginated_qs = paginator.paginate_queryset(qs, request)
    serializer = FleekSerializer(paginated_qs, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data) # Response( serializer.data, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fleeks_feed_view(request, *args, **kwargs):

    userids  = [request.user.id]


    for fleeker in request.user.profile.following.all():
        userids.append(fleeker.id)
    
    fleeks = Fleek.objects.filter(user__id__in=userids)

    # for oink in oinks:
    #     likes = oink.likes.filter(created_by_id=request.user.id)

    #     if likes.count() > 0:
    #         oink.liked = True
    #     else:
    #         oink.liked = False

    return get_paginated_queryset_response(fleeks, request)

# def get_queryset(self):
#     user = self.request.user
#     qs = Follow.objects.filter(user=user)
#     follows = [user]
#     for obj in qs:
#         follows.append(obj.follow_user)
#     return Post.objects.filter(author__in=follows).order_by('-date_posted')


    # qs = Fleek.objects.feed(user)
    # return get_paginated_queryset_response(qs, request)

@api_view(['GET'])
def fleeks_list_view(request, *args, **kwargs):
    qs = Fleek.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.by_username(username)
    return get_paginated_queryset_response(qs, request)



# def tweet_create_view_pure_django(request, *args, **kwargs):
#     '''
#     REST API Create View -> DRF
#     '''
#     user = request.user
#     if not request.user.is_authenticated:
#         user = None
#         if request.is_ajax():
#             return JsonResponse({}, status=401)
#         return redirect(settings.LOGIN_URL)
#     form = TweetForm(request.POST or None)
#     next_url = request.POST.get("next") or None
#     if form.is_valid():
#         obj = form.save(commit=False)
#         # do other form related logic
#         obj.user = user
#         obj.save()
#         if request.is_ajax():
#             return JsonResponse(obj.serialize(), status=201) # 201 == created items
#         if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
#             return redirect(next_url)
#         form = TweetForm()
#     if form.errors:
#         if request.is_ajax():
#             return JsonResponse(form.errors, status=400)
#     return render(request, 'components/form.html', context={"form": form})


# def tweet_list_view_pure_django(request, *args, **kwargs):
#     """
#     REST API VIEW
#     Consume by JavaScript or Swift/Java/iOS/Andriod
#     return json data
#     """
#     qs = Tweet.objects.all()
#     tweets_list = [x.serialize() for x in qs]
#     data = {
#         "isUser": False,
#         "response": tweets_list
#     }
#     return JsonResponse(data)


# def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
#     """
#     REST API VIEW
#     Consume by JavaScript or Swift/Java/iOS/Andriod
#     return json data
#     """
#     data = {
#         "id": tweet_id,
#     }
#     status = 200
#     try:
#         obj = Tweet.objects.get(id=tweet_id)
#         data['content'] = obj.content
#     except:
#         data['message'] = "Not found"
#         status = 404
#     return JsonResponse(data, status=status) # json.dumps content_type='application/json'