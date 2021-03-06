from django.shortcuts import render
from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .utils import MultipartJsonParser
from .renderers import JPEGRenderer, PNGRenderer
from rest_framework.exceptions import NotAcceptable
from rest_framework import status, generics
from django.shortcuts import get_list_or_404, get_object_or_404
from core.renderers import CoreJSONRenderer
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from fcm_django.models import FCMDevice
from push_notifications.models import APNSDevice, GCMDevice,  WebPushDevice
from rest_framework import generics
from django.db.models import Q, Count
from rest_framework.filters import SearchFilter, OrderingFilter 
import rest_framework_filters as filters
from django.contrib.gis.db.models.functions import GeometryDistance, Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models import F
from itertools import chain
from authentication.models import User
import random
import datetime



from discover.models import (
    Category,
    Product,
    PaymentMethod,
    PurchaseOrder,
    PurchaseItem,
    Post,
    ProductImage,
    ViewsNumber
)
from discover.serializers import (
    CategorySerializer,
    ProductSerializer,
    PaymentMethodSerializer,
    PurchaseOrderSerializer,
    PurchaseItemSerializer,
    PostSerializer,
    ProductImageSerializer,
    Product_ImageSerializer,

)









class ProductFilter(filters.FilterSet):


    class Meta:
        model = Product
        fields = {'title': ['exact', 'in', 'startswith'],
                  'category__name': ['exact', 'in', 'startswith'],
                  'price': ['exact', 'gt', 'lt']
                 }

class PostFilter(filters.FilterSet):
    # Not overridden by `__all__`
    #price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt', label='Minimum price')
    # product__title = filters.CharFilter(field_name='product__title',lookup_expr='exact',  label='product title')
    #product__title = filters.CharFilter(field_name='product__title',lookup_expr='in',  label='product title')
    product = filters.RelatedFilter( ProductFilter, field_name='product', queryset=Product.objects.all())

    # price__gt = filters.NumberFilter(field_name='product__price', lookup_expr='gt', label='Minimum price')
    # price__lt = filters.NumberFilter(field_name='product__price', lookup_expr='lt', label='Maxmum price')
    # prod_title__startwith = filters.CharFilter(field_name='product__title', lookup_expr='startswith', label='product title')
    # prod_title__exact = filters.CharFilter(field_name='product__title', lookup_expr='exact', label='product title')
    # product__category = filters.CharFilter(field_name='product__category__name',lookup_expr=('startswith', 'exact', 'in') ,  label='product category')

    class Meta:
        model = Post
        fields = {
            'product': '__all__' ,
        }




class PostViaLocationView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_class = PostFilter


    def get_queryset(self, *args, **kwargs):
        #begin by getting the users location and display post within 100km radio of that geo pointfield.

        ref_location = Point(-32.7218138, 152.1440889, srid=4326)
        qp_latitude = self.request.query_params.get('latitude', None)
        latitude = float(qp_latitude)
        qp_longitude = self.request.query_params.get('longitude', None)
        longitude = float(qp_longitude)
        within_distance_ref = self.request.query_params.get('with', None)
        user_ref_location = Point(longitude, latitude, srid=4326)


        if  within_distance_ref is not None:
            resdata = Post.objects.filter(location__dwithin=( user_ref_location, D(km=within_distance_ref) )).annotate(distance=GeometryDistance("location",  user_ref_location))\
            .order_by("distance")

        if within_distance_ref is None:

            resdata = Post.objects.filter(location__dwithin=( user_ref_location,  D(km=200))).annotate(distance=Distance("location",  user_ref_location))\
            .order_by("distance")
            
        return  resdata
    

#View for displaying users posts within a specified distance.

class PostLocation(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_class = PostFilter


    def get_queryset(self, *args, **kwargs):

        ref_location = Point(-32.7218138, 152.1440889, srid=4326)   # Default ref_location point/if current user's gps is unavailable.

        # Latitude and longitude coordinates from user's gps: client side.
        qp_latitude = self.request.query_params.get('latitude', None)
        if qp_latitude is not None:
            if qp_latitude == 'undefined':
                latitude = float('-32.7218138')
            else:
                latitude = float(qp_latitude)
        

        qp_longitude = self.request.query_params.get('longitude', None)
        if qp_longitude is not None:
            if qp_longitude == 'undefined':
                longitude = float('152.1440889')
            else:
                longitude = float(qp_longitude)
                
                

        user_ref_location = Point(longitude, latitude, srid=4326)
        
        # user's specified search radius. checking if a distance radius was given
        within_distance_ref = self.request.query_params.get('with', None)

        if  within_distance_ref is not None:
            resdata = Post.objects.filter(location__dwithin=( user_ref_location, D(km=within_distance_ref) )).annotate(distance=GeometryDistance("location",  user_ref_location))\
            .order_by("distance")

        # If a search distance was  not provided, 200km radius is placed as the Default search radius.
        if within_distance_ref is None:
            resdata = Post.objects.filter(location__dwithin=( user_ref_location,  D(km=200))).annotate(distance=Distance("location",  user_ref_location))\
            .order_by("distance")
            



        queryset = resdata

        title__startswith = self.request.query_params.get('title__startswith', None)
        title__in = self.request.query_params.get('title__in', None)
        title__exact = self.request.query_params.get('title__exact', None)

        category__startswith = self.request.query_params.get('category__startswith', None)
        category__in = self.request.query_params.get('category__in', None)
        category__exact = self.request.query_params.get('category__exact', None)

        taggit__startswith = self.request.query_params.get('taggit__startswith', None)
        taggit__name__startswith = self.request.query_params.get('taggit__name__startswith', None)

        price__lt = self.request.query_params.get('price__lt', None)
        price__gt = self.request.query_params.get('price__gt', None)
        price__exact = self.request.query_params.get('price__exact', None)

        QueryEmpty = False
        AutoSearch = True

        if title__startswith is not None:
            
            if title__startswith == 'None':
                #no maximum price was given
                pass
            else:
                newqueryset = queryset.filter(product__title__startswith=title__startswith.lower())
                if not newqueryset.exists():
                    AutoSearch = False
                    pass
                else:
                    QueryEmpty = True
                    queryset = newqueryset


        if title__in is not None:

            if title__startswith == 'None':
                #no maximum price was given
                pass
            else:
                newqueryset = queryset.filter(product__title__in=title__startswith.lower())
                if not newqueryset.exists():
                    AutoSearch = False
                    pass
                else:
                    QueryEmpty = True
                    queryset = newqueryset
        if title__exact is not None:

            if title__startswith == 'None':
                #no maximum price was given
                pass
            else:
                newqueryset = queryset.filter(product__title__exact=title__startswith.lower())
                if not newqueryset.exists():
                    AutoSearch = False
                    pass
                else:
                    QueryEmpty = True
                    queryset = newqueryset

        if price__gt is not None:
            if price__gt == 'None':
                #no minimum price was given
                pass
            else:
                queryset = queryset.filter(product__price__gt=price__gt)

            
        if price__lt is not None:
            if price__lt == 'None':
                #no maximum price was given
                pass
            else:
                queryset = queryset.filter(product__price__lt=price__lt) 
             
        if price__exact is not None:
            queryset = queryset.filter(product__price__exact=price__exact)  

        if category__startswith is not None:
            queryset = queryset.filter(product__category__startswith=category__startswith)
        if category__in is not None:
            queryset = queryset.filter(product__category__in=category__in)
        if category__exact is not None:
            if category__exact == 'None':
               pass
            else:
                queryset = queryset.filter(product__category__exact=category__exact)
        
        # if taggit__startswith is not None:
        #     if taggit__startswith == 'None':
        #         pass
        #     else:
        #         queryset = queryset.filter(product__taggit__name=taggit__startswith)

        if AutoSearch == False:

            EmptySet = Post.objects.none()
            queryset = EmptySet
            combined_result = None
        if AutoSearch == True:
            combined_result = queryset

        
        if taggit__name__startswith is not None:
            if taggit__name__startswith == 'None':
                pass
            else:
                tagsQueryset = Post.objects.filter(product__taggit__name__startswith=taggit__name__startswith.lower())
                print('This is Tags queryset', tagsQueryset)
                if not tagsQueryset.exists():
                    combined_result = None
                    pass
                else:
                    combined_results = tagsQueryset
                    combined_result = combined_results

        print("IIIIITS", combined_result)

        
    
        return combined_result



class  PostsAndroidAPI(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_class = PostFilter

    def get(self, request):

        ref_location = Point(-32.7218138, 152.1440889, srid=4326)   # Default ref_location point/if current user's gps is unavailable.

        # Latitude and longitude coordinates from user's gps: client side.
        qp_latitude = self.request.query_params.get('latitude', None)
        if qp_latitude is not None:
            if qp_latitude == 'undefined':
                latitude = float('-32.7218138')
            else:
                latitude = float(qp_latitude)
        

        qp_longitude = self.request.query_params.get('longitude', None)
        if qp_longitude is not None:
            if qp_longitude == 'undefined':
                longitude = float('152.1440889')
            else:
                longitude = float(qp_longitude)
                
                

        user_ref_location = Point(longitude, latitude, srid=4326)
        
        # user's specified search radius. checking if a distance radius was given
        within_distance_ref = self.request.query_params.get('with', None)

        if  within_distance_ref is not None:
            resdata = Post.objects.filter(location__dwithin=( user_ref_location, D(km=within_distance_ref) )).annotate(distance=GeometryDistance("location",  user_ref_location))\
            .order_by("distance")

        # If a search distance was  not provided, 200km radius is placed as the Default search radius.
        if within_distance_ref is None:
            resdata = Post.objects.filter(location__dwithin=( user_ref_location,  D(km=200))).annotate(distance=Distance("location",  user_ref_location))\
            .order_by("distance")
            



        queryset = resdata

        title__startswith = self.request.query_params.get('title__startswith', None)
        title__in = self.request.query_params.get('title__in', None)
        title__exact = self.request.query_params.get('title__exact', None)

        category__startswith = self.request.query_params.get('category__startswith', None)
        category__in = self.request.query_params.get('category__in', None)
        category__exact = self.request.query_params.get('category__exact', None)

        taggit__startswith = self.request.query_params.get('taggit__startswith', None)
        taggit__name__startswith = self.request.query_params.get('taggit__name__startswith', None)

        price__lt = self.request.query_params.get('price__lt', None)
        price__gt = self.request.query_params.get('price__gt', None)
        price__exact = self.request.query_params.get('price__exact', None)

        QueryEmpty = False
        AutoSearch = True

        if title__startswith is not None:
            
            if title__startswith == 'None':
                #no maximum price was given
                pass
            else:
                newqueryset = queryset.filter(product__title__startswith=title__startswith.lower())
                if not newqueryset.exists():
                    AutoSearch = False
                    pass
                else:
                    QueryEmpty = True
                    queryset = newqueryset


        if title__in is not None:

            if title__startswith == 'None':
                #no maximum price was given
                pass
            else:
                newqueryset = queryset.filter(product__title__in=title__startswith.lower())
                if not newqueryset.exists():
                    AutoSearch = False
                    pass
                else:
                    QueryEmpty = True
                    queryset = newqueryset
        if title__exact is not None:

            if title__startswith == 'None':
                #no maximum price was given
                pass
            else:
                newqueryset = queryset.filter(product__title__exact=title__startswith.lower())
                if not newqueryset.exists():
                    AutoSearch = False
                    pass
                else:
                    QueryEmpty = True
                    queryset = newqueryset

        if price__gt is not None:
            if price__gt == 'None':
                #no minimum price was given
                pass
            else:
                queryset = queryset.filter(product__price__gt=price__gt)

            
        if price__lt is not None:
            if price__lt == 'None':
                #no maximum price was given
                pass
            else:
                queryset = queryset.filter(product__price__lt=price__lt) 
             
        if price__exact is not None:
            queryset = queryset.filter(product__price__exact=price__exact)  

        if category__startswith is not None:
            queryset = queryset.filter(product__category__startswith=category__startswith)
        if category__in is not None:
            queryset = queryset.filter(product__category__in=category__in)
        if category__exact is not None:
            if category__exact == 'None':
               pass
            else:
                queryset = queryset.filter(product__category__exact=category__exact)
        
        # if taggit__startswith is not None:
        #     if taggit__startswith == 'None':
        #         pass
        #     else:
        #         queryset = queryset.filter(product__taggit__name=taggit__startswith)

        if AutoSearch == False:

            EmptySet = Post.objects.none()
            queryset = EmptySet
            combined_result = None
        if AutoSearch == True:
            combined_result = queryset

        
        if taggit__name__startswith is not None:
            if taggit__name__startswith == 'None':
                pass
            else:
                tagsQueryset = Post.objects.filter(product__taggit__name__startswith=taggit__name__startswith.lower())
                print('This is Tags queryset', tagsQueryset)
                if not tagsQueryset.exists():
                    combined_result = None
                    pass
                else:
                    combined_results = tagsQueryset
                    combined_result = combined_results


        postSerializedData = PostSerializer(data=combined_result, many=True)
        postSerializedData.is_valid()
        
        randomID = random.randint(0,100000)
        date = datetime.datetime.now()
        resultsData = {}
        resultsData["id"] = 1
        resultsData["lastRefresh"] = date
        resultsData["results"] = postSerializedData.data

        return Response(resultsData)






class PostSearchView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    filter_class = PostFilter

    def get_queryset(self, *args, **kwargs):

        queryset = Post.objects.all()

        title__startswith = self.request.query_params.get('title__startswith', None)
        title__in = self.request.query_params.get('title__in', None)
        title__exact = self.request.query_params.get('title__exact', None)

        category__startswith = self.request.query_params.get('category__startswith', None)
        category__in = self.request.query_params.get('category__in', None)
        category__exact = self.request.query_params.get('category__exact', None)

        price__lt = self.request.query_params.get('price__lt', None)
        price__gt = self.request.query_params.get('price__gt', None)
        price__exact = self.request.query_params.get('price__exact', None)

        if title__startswith is not None:
            queryset = queryset.filter(product__title__startswith=title__startswith)
        if title__in is not None:
            queryset = queryset.filter(product__title__in=title__in)
        if title__exact is not None:
            queryset = queryset.filter(product__title__exact=title__exact)

        if price__gt is not None:
            queryset = queryset.filter(product__price__gt=price__gt)
        if price__lt is not None:
            queryset = queryset.filter(product__price__lt=price__lt)  
        if price__exact is not None:
            queryset = queryset.filter(product__price__exact=price__exact)  

        if category__startswith is not None:
            queryset = queryset.filter(product__category__startswith=category__startswith)
        if category__in is not None:
            queryset = queryset.filter(product__category__in=category__in)
        if category__exact is not None:
            queryset = queryset.filter(product__category__exact=category__exact)
    
        return queryset



    

class  SearchPost(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [PostFilter,]
    queryset = Post.objects.all()




class PostCreatView(ModelViewSet):

    
    permission_classes = (IsAuthenticated,)  
    queryset = Category.objects.all()
    serializer_class = PostSerializer
    parser_classes = [MultipartJsonParser, JSONParser,]

    
    

    def get_serializer_context(self):
        context = super(PostCreatView, self).get_serializer_context()
        print('cont', self.request.data)
        product = Product.objects.filter(id = 16)
    

        if len(self.request.data) > 0:
            context.update({
                'included_images': self.request.data
            })
            context.update({
                'location_info': self.request.data
            })

        return context
        
    def create(self, request, id, *args, **kwargs):


        serializer = self.get_serializer(data=request.data)
        
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print('this is pre-save serializery', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer,


    def get(self, request, format=None):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)

        return JsonResponse(serializer.data)




class  ProfileUserPostsAndroidAPI(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request):

        posts = Post.objects.filter(owner=request.user.id)
        print("this is posts", posts)
        serializer = PostSerializer(posts, many=True)
       
        #random Id 
        randomID = random.randint(0,100000)
        #DateTime upon requests
        date = datetime.datetime.now()
        #Dictionary Results Data
        resultsData = {}
        resultsData["id"] = 1
        resultsData["lastRefresh"] = date
        resultsData["results"] = serializer.data

        return Response(resultsData)


class  UserPostsAndroidAPI(APIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, id):
        posts = Post.objects.filter(owner=id)
        serializer = PostSerializer(posts, many=True)
       
        #random Id 
        randomID = random.randint(0,100000)
        #DateTime upon requests
        date = datetime.datetime.now()
        #Dictionary Results Data
        resultsData = {}
        resultsData["id"] = randomID
        resultsData["lastRefresh"] = date
        resultsData["results"] = serializer.data

        return Response(resultsData)


@csrf_exempt
def ProfileUserListings(request, id):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        
        posts = Post.objects.filter(owner=id)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)



  
  

class PostDetailView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        posts = super(PostDetailView, self).get_queryset()
        post_data = posts.filter(id=self.kwargs['id'])
        post = post_data[0]
        print('this is post',post)

        #Check whether the current user has view the post
        Checkview_Q = ViewsNumber.objects.filter(post__id=self.kwargs['id'])
        Checkviews = Checkview_Q[0]
        num_results = ViewsNumber.objects.filter(post__id=self.kwargs['id']).count()
        print('this is numre',Checkviews.user.all())
        currentUser = User.objects.get(id=self.request.user.id)
     

        if num_results <= 0:
            pass
        else:
            userCheck_data = Checkviews.user.all()

            if currentUser in userCheck_data:
                pass
            
            else:
                Checkviews.numberview = Checkviews.numberview+1
                post.viewcount = post.viewcount+1
                post.save()
                Checkviews.user.add(currentUser)
                Checkviews.save()


 

        return post_data
         
    




class Post_DetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get(self, pk, request, format=None):
        queryset = Post.objects.all()
        print('this is queryset', queryset)
        serializer = PostSerializer(queryset)

        return Response(queryset)

class UserPostView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Post.objects.filter(owner = self.request.user.id)
        return queryset

class  UserDeletePostView(APIView):
    permission_classes = (IsAuthenticated,) 

    def delete(self, request, pk, format=None):
        queryset = Post.objects.filter(owner = self.request.user.id, pk=pk ).delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class Postfilterview(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):



        category = self.kwargs['category']


        prod = self.request.data

        return Post.objects.filter(product__category=category)

#----------------------------------end-post
class CategoryView(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    queryset = None 


    def get_queryset(self):
        context = super(CategoryView, self).get_queryset()
   
        product_set = context

        return product_set






class CategoryCreateView(CreateAPIView):
    # Create view for Category objects

    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'description' 




#----------------------------------end-Category


class  UserDeleteProductView(APIView):
    permission_classes = (IsAuthenticated,) 

    def delete(self, request, pk, format=None):
        queryset = Product.objects.filter(user = self.request.user.id, pk=pk ).delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)

    



class UserProductView(ModelViewSet):
    permission_classes = (IsAuthenticated,) 

    serializer_class = ProductSerializer
    parser_classes = [MultipartJsonParser, JSONParser,]

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(user = self.request.user, listed=False)

        return queryset

@csrf_exempt
def Product_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        product =  Product.objects.all() 
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)
@csrf_exempt
def Product_listCategory(request, category):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        product =  Product.objects.filter(category=category)
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False)




class ProductCreateView(ModelViewSet):
    # Create view for Category objects

    permission_classes = (IsAuthenticated,)  
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultipartJsonParser, JSONParser,]

    def get_serializer_context(self):
        context = super(ProductCreateView, self).get_serializer_context()
 
        if len(self.request.data) > 0:
            context.update({
                'included_images': self.request.FILES
            })

            context.update({
                'category_info': self.request.data
            })


        return context

    def create(self, request, *args, **kwargs):

        try:
            PostImage_serializer = ProductImageSerializer(data=request.FILES)
            PostImage_serializer.is_valid(raise_exception=True)
        except Exception:
            raise NotAcceptable(

                detail={
                    'message': 'upload a valid image. The file you uploaded was '
                                'neither not an image or a corrupted image.'
                }, code=406
            )
        print('this is new request data', request.data)
        serializer = self.get_serializer(data=request.data)
        
        
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@csrf_exempt
def Product_image_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        product_image = ProductImage.objects.all()
        serializer = Product_ImageSerializer(data=product_image, context={'request': request}, many=True)
        serializer.is_valid()
        return JsonResponse(serializer.data, safe=False)

class ProductImageViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
 
    serializer_class = Product_ImageSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = ProductImage.objects.all()

        return queryset







class  ProductImageset(APIView):
    permission_classes = (AllowAny, )
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()

    def get(self, request, id,):
        queryset = ProductImage.objects.all()
        images = queryset.filter(product_id= id)
        
        lists = list(images)

        print(lists)
        cont = {}
        productimages = []
        for i in lists:
            condo = i.product.id
            prod_barcode = i.product.barcode
            prod_title = i.product.title
            prod_description = i.product.description
            prod_price = i.product.price
            prod_category = i.product.category
            prod_slug = i.product.slug

            product = {}
            product.update({'jesys':prod_barcode})
            product.update({'title': prod_title})
            product.update({'description': prod_description})
            product.update({'price': prod_price})
            product.update({'category': prod_category})
            product.update({'slug': prod_slug})


            print('this is IIII',product)
            cont.update({
                'product': product,
                'user': i.user,
                'image': i.image
            })
            serializer = Product_ImageSerializer(data=cont)
            serializer.is_valid()

            product.update({'productimage': serializer.data})
            productimages.append( {'product': product})
     
           
        
        print('hello there',productimages)
        return Response(productimages)
        

#-------------------------------end-Product

class PaymentMethodCreateView(CreateAPIView):
    # Create view for PaymentMethod objects

    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    lookup_field = 'description'


class PurchaseOrderCreateView(CreateAPIView):
    # Create view for PurchaseOrder objects

    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'id'


class PurchaseItemCreateView(CreateAPIView):
    # Create view for PurchaseItem objects 

    queryset = PurchaseItem.objects.all()
    serializer_class = PurchaseItemSerializer
    lookup_field = 'id'
