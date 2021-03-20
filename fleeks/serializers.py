
from django.conf import settings
from rest_framework import serializers
from django.forms import ImageField as DjangoImageField

from core.serializers import ProfileSerializer
from authentication.serializers import UserSerializer
from .models import Fleeka, FleeksImage
from authentication.models import User

MAX_FLEEK_LENGTH = settings.MAX_FLEEK_LENGTH 
FLEEK_ACTION_OPTIONS = settings.FLEEK_ACTION_OPTIONS




class Fleek_ImageSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedRelatedField(view_name="fleeks:fleeksimage-detail", read_only=True, lookup_field="fleeksimage")
    fleek = serializers.HyperlinkedRelatedField(view_name="fleeks:fleek-detail", read_only=True, source="user__user" )
    user = UserSerializer(read_only=True) 

    class Meta:
        model = FleeksImage
        fields =['id', 'fleek','url', 'image', 'created', 'user']
        extra_kwargs = { 
            'fleek': {'required': False},
        }
 


class FleekImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedRelatedField(view_name="fleeks:fleeksimage-detail", read_only=True, lookup_field="fleeksimage")
    fleek = serializers.HyperlinkedRelatedField(view_name="fleeks:fleek-detail", read_only=True)
    #fleek_id = serializers.CharField(source='fleek_id', read_only=True)
    user = UserSerializer(read_only=True) 

    class Meta:
        model = FleeksImage
        fields =['id', 'fleek','url', 'user',  'image', 'created',]
        extra_kwargs = { 
            'fleek': {'required': False},
            'url': {'view_name': 'fleeks:fleeksimage-detail'}, 
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

class FleekSerializer(serializers.HyperlinkedModelSerializer):

    fleeksimage_set = Fleek_ImageSerializer(allow_null=True, many=True, read_only=True)
    user = UserSerializer(read_only=True) 
    url = serializers.HyperlinkedRelatedField(view_name="fleeks:fleek-detail", read_only=True, lookup_field="pk")

    class Meta:
        """ fleekSerializer's Meta class """
        model = Fleeka
        fields = ["id",'url', "created", 'anonymity', 'public',  'fleeksimage_set', "content", "user"]
        extra_kwargs = {
            'fleek_image_set': {'view_name': 'fleeks:fleekimage-detail'},
        }


    def create(self, validated_data):
        print("oooo")
        data = self.context['fleeks_info']
        #profile = Profile.objects.get(user = self.context['request'].user)
        user_instance = User.objects.get(id = self.context['request'].user.id)


        fleek_obj = Fleek.objects.get_or_create(
            content = validated_data['content'],
            user =  user_instance,
        )

        fleek_ = fleek_obj[0]
        print("\\\\\\",fleek_.id)
        
        fleek_instance = Fleek.objects.get(id=fleek_.id)

        images_data = self.context['included_images']
        
        for i in images_data.getlist('image'):
            FleeksImage.objects.create(fleek=fleek_instance, image=i,  user=user_instance)
        return fleek_obj
               



class FleekActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in FLEEK_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for fleeks")
        return value


class FleekCreateSerializer(serializers.ModelSerializer):
    user = ProfileSerializer(read_only=True) 

    
    class Meta:
        model = Fleeka
        fields = ['user', 'id', 'content','created', 'parent', 'is_refleek']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        
        if len(value) > MAX_FLEEK_LENGTH :
            raise serializers.ValidationError("This fleek is too long")
        return value

    # def get_user(self, obj):
    #     return obj.user.id


# class FleekSerializer(serializers.ModelSerializer):
#     user = ProfileSerializer( read_only=True) 
#     likes = serializers.SerializerMethodField(read_only=True)
#     parent = FleekCreateSerializer(read_only=True)
#     class Meta:
#         model = Fleek
#         fields = [
#                 'user', 
#                 'id', 
#                 'content',
#                 'likes',
#                 'is_refleek',
#                 'parent',
#                 'created']

#     def get_likes(self, obj):
#         return obj.likes.count()