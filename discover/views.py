from django.shortcuts import render
from django.db.models import Q

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

from discover.models import (
    Category,
    Product,
    PaymentMethod,
    PurchaseOrder,
    PurchaseItem,
    Post,
    ProductImage
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


class PostCreatView(ModelViewSet):
    # Create view for Category objects

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


class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer,


    def get(self, request, format=None):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)

        return JsonResponse(serializer.data)


@csrf_exempt
def Post_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':

        device = GCMDevice.objects.all()
        print('this is another pus', device)
        
        device.send_message("This is a message")


        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)




class PostDetailView(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        posts = super(PostDetailView, self).get_queryset()
        print(self.kwargs['id'])
        post = posts.filter(id=self.kwargs['id'])
        print('this is post',post)
        return post
         
    




class Post_DetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    #queryset = Post.objects.all()

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

#----------------------------------end-post
class CategoryView(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self, *args, **kwargs):
        col = Category.objects.all()

        return col


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
        queryset = Product.objects.filter(user = self.request.user)

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

# def Product_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         product = Product.objects.all()
#         serializer = ProductSerializer(product, many=True)
#         return JsonResponse(serializer.data, safe=False)


class ProductCreateView(ModelViewSet):
    # Create view for Category objects

    permission_classes = (IsAuthenticated,)  # you are here
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = [MultipartJsonParser, JSONParser,]

    def get_serializer_context(self):
        context = super(ProductCreateView, self).get_serializer_context()
 
        if len(self.request.data) > 0:
            context.update({
                'included_images': self.request.FILES
            })

            # print('this is your context', self.request.data)
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

# class ProductImageViewSet(ModelViewSet):
#     permission_classes = (IsAuthenticated,)
 
#     serializer_class = ProductSerializer

#     def get_queryset(self, *args, **kwargs):
#         queryset = Product.objects.all()

#         return queryset





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
