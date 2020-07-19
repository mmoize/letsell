from rest_framework import serializers

from discover.models import (
    Category,
    Product,
    PaymentMethod,
    PurchaseOrder,
    PurchaseItem,
    Tags,
    Post,
    ProductImage
)
from authentication.models import User
from authentication.serializers import UserSerializer
from taggit.models import Tag
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)
from django.forms import ImageField as DjangoImageField
from rest_framework.exceptions import NotAcceptable   


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for the Category model """

    class Meta:
        """ CategorySerializer's Meta class """

        model = Category
        fields = '__all__'

class TagsSerializer(serializers.HyperlinkedModelSerializer):        
         
    class Meta:
        model = Tags
        fields = [ 'url','name', 'pk']

class Product_ImageSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedRelatedField(view_name="discover:productimage-detail", read_only=True, lookup_field="productimage")
    product = serializers.HyperlinkedRelatedField(view_name="discover:product-detail", read_only=True, source="product_user" )
    products_id = serializers.CharField(source='product_id', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductImage
        fields =['id', 'product','url','pk', 'products_id', 'image', 'created', 'user']
        extra_kwargs = { 
            'product': {'required': False},
            'products_id': {'required': False},
            # 'url': {'view_name': 'discover:productimage-detail'}, 
        }
 


class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    #url = serializers.HyperlinkedIdentityField(view_name="discover:productimage-detail",  source="productimage")
    url = serializers.HyperlinkedRelatedField(view_name="discover:productimage-detail", read_only=True, lookup_field="productimage")
    product = serializers.HyperlinkedRelatedField(view_name="discover:product-detail", read_only=True, source="product_user" )
    products_id = serializers.CharField(source='product_id', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductImage
        fields =['id', 'product','url', 'products_id', 'image', 'created', 'user']
        extra_kwargs = { 
            'product': {'required': False},
            'products_id': {'required': False},
            # 'url': {'view_name': 'discover:productimage-detail'}, 
        }
 
    
    def validate(self, attrs):
    
        default_error_messages = {
            'invalid_image':
            'Upload a valid image. The file you uploaded was either not an image'
        }

        for i in self.initial_data.getlist('image'):
            django_field = DjangoImageField()
            django_field.error_messages = default_error_messages
            django_field.clean(i)
        return attrs

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    """ Serializer for the Product model """
    tags = TagsSerializer( allow_null=True, many=True, read_only=True)
    user = UserSerializer(read_only=True)
    taggit = TagListSerializerField(allow_null=True, required=False)
    #product_image_set = serializers.HyperlinkedRelatedField(view_name="discover:productimage-detail", read_only=True)
    product_image_set = ProductImageSerializer(allow_null=True, many=True, read_only=True)
    url = serializers.HyperlinkedRelatedField(view_name="discover:product-detail", read_only=True, lookup_field="product_user")
    # category = CategorySerializer()
    class Meta:
        """ ProductSerializer's Meta class """

        model = Product
        fields = ["tags","taggit","id",'url', "created", "title", 'product_image_set', "description", "price", "barcode", "slug", "category", "user"]


    def create(self, validated_data):

        
        try:
            
            product_obj = Product.objects.create(
                title = validated_data['title'],
                description = validated_data['description'],
                price = validated_data['price'],
                barcode = validated_data['barcode'],
                category = validated_data['category'],
                slug = validated_data['slug'],
                user = self.context['request'].user
            )

            # if 'included_images' in self.context:
                
            #     images_data = self.context['included_images']
            #     for i in images_data.getlist('image'):
            #         print("another", i)
            #         ProductImage.objects.create(product=product_obj, image=i,  user=self.context['request'].user)

        except Exception:
            raise NotAcceptable(
                detail={
                    'message': 'The request is not acceptable.'
                }, code=406)



        images_data = self.context['included_images']
        for i in images_data.getlist('image'):
            print("another", i)
            ProductImage.objects.create(product=product_obj, image=i,  user=self.context['request'].user)

        if 'taggit' in validated_data:
            taggit_data = validated_data.pop('taggit')
            for taggit_data in taggit_data:
                taggit_obj, created = Tag.objects.get_or_create(name=taggit_data)
                product_obj.taggit.add(taggit_obj)
        
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            for tags_data in tags_data:
                for i in tags_data.items():
                    tags_obj, created = Tags.objects.get_or_create(name=i[1])
                    product_obj.tags.add(tags_obj)

        return product_obj
        

        



class PostSerializer(serializers.HyperlinkedModelSerializer, TaggitSerializer):
    url = serializers.HyperlinkedRelatedField(view_name="discover:post_create-detail", read_only=True)
    owner = UserSerializer(read_only=True,)
    product_image_set = ProductImageSerializer(many=True, read_only=True )
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('url', 'id','product','owner', 'product_image_set', 'created_at', 'updated_at', 'latitude', 'longitude',)
        # fields = '__all__'
        extra_kwargs = { 
            'owner': {'required': False}
        }
    
   
    def create(self, validated_data):

        try:
            
            post_obj = Post.objects.create(
                latitude = validated_data['latitude'],
                longitude = validated_data['longitude'],
                # product = validated_data['product'],
                owner = self.context['request'].user
            )
    
        except Exception:
            raise NotAcceptable(
                detail={
                    'message': 'The request is not acceptable.'
                }, code=406)
        prod = self.context['included_images']
        titles = prod['title']
        slugs = prod['slug']
        print('skug', slugs)
        try:

            product_obj, created = Product.objects.get_or_create(
                title = titles,

                slug = slugs,
                user = self.context['request'].user
            )
            post_obj.product.add(product_obj)

            
    
        except Exception:
            raise NotAcceptable(
                detail={
                    'message': 'The request is not acceptable. prod'
                }, code=406)

        return post_obj








class PaymentMethodSerializer(serializers.ModelSerializer):
    """ Serializer for the PaymentMethod model """

    class Meta:
        """ PaymentMethodSerializer's Meta class """

        model = PaymentMethod
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    """ Serializer for the PurchaseOrder model """

    class Meta:
        """ PurchaseOrderSerializer's Meta class """

        model = PurchaseOrder
        fields = '__all__'


class PurchaseItemSerializer(serializers.ModelSerializer):
    """ Serializer for the PurchaseItem model """

    class Meta:
        """ PurchaseItemSerializer's Meta class """

        model = PurchaseItem
        fields = '__all__'


                