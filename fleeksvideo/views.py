from django.shortcuts import render
from django.db.models import Q


from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )



from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from .models import Fleek, Comment

from .pagination import FleekLimitOffsetPagination, FleekPageNumberPagination
#from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    FleekCreateUpdateSerializer, 
    FleekDetailSerializer, 
    FleekListSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
    FleekActionSerializer
    )


class FleekCreateAPIView(CreateAPIView):
    queryset = Fleek.objects.all()
    serializer_class = FleekCreateUpdateSerializer
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FleekDetailAPIView(RetrieveAPIView):
    queryset = Fleek.objects.all()
    serializer_class = FleekDetailSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    #lookup_url_kwarg = "abc"


class FleekUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Fleek.objects.all()
    serializer_class = FleekCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticated, )
    #permission_classes = [IsOwnerOrReadOnly]
    #lookup_url_kwarg = "abc"
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        #email send_email



class FleekDeleteAPIView(DestroyAPIView):
    queryset = Fleek.objects.all()
    serializer_class = FleekDetailSerializer
    lookup_field = 'slug'
    #permission_classes = [IsOwnerOrReadOnly]
    #lookup_url_kwarg = "abc"


class FleekListAPIView(ListAPIView):
    serializer_class = FleekListSerializer
    filter_backends= [SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    search_fields = ['title', 'description', 'user__username']
    pagination_class = FleekPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Fleek.objects.all() #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(description__icontains=query)|
                    Q(user__username__icontains=query) |
                    Q(user__first_name__icontains=query)
                    ).distinct()
        return queryset_list






class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    #serializer_class = create_comment_serializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        print("its model_type", model_type)
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type, 
                slug=slug, 
                parent_id=parent_id,
                user=self.request.user
                )

    # def perform_create(self, serializer):
    # serializer.save(user=self.request.user)


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    #permission_classes = [IsOwnerOrReadOnly]
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     #lookup_url_kwarg = "abc"
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)
#         #email send_email



# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     #lookup_url_kwarg = "abc"


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = (AllowAny, )
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = FleekPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Comment.objects.filter(id__gte=0) #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list




#@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fleek_action_view(request, *args, **kwargs):
    '''
    id is required.
    Action options are: like, unlike
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
            obj.likes.add(request.user)
            serializer = FleekDetailSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike":
            obj.likes.remove(request.user)
            serializer = FleekDetailSerializer(obj)
            return Response(serializer.data, status=200)
        # elif action == "refleek":
        #     new_fleek = Fleek.objects.create(
        #             user=request.user, 
        #             parent=obj,
        #             content=content,
        #             )
        #     serializer = FleekSerializer(new_fleek)
        #     return Response(serializer.data, status=201)
    return Response({}, status=200)