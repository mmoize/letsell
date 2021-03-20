from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )


from rest_framework import serializers
from .models import Fleek, Comment
from authentication.serializers import UserSerializer
FLEEK_ACTION_OPTIONS = settings.FLEEK_ACTION_OPTIONS




class FleekActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate_action(self, value):
        value = value.lower().strip() # "Like " -> "like"
        if not value in FLEEK_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for FLEEKS")
        return value




class FleekCreateUpdateSerializer(ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Fleek
        fields = [
            'id',
            'title',
            'likes',
            'description',
            'videoUrl',
            'musicCoverTitle',
            'publish'
        ]

    def get_likes(self, obj):
        return obj.likes.count()


fleek_detail_url = HyperlinkedIdentityField(
        view_name='fleeks-api:detail',
        lookup_field='slug'
        )


class FleekDetailSerializer(serializers.HyperlinkedModelSerializer):
    #url = fleek_detail_url
    url = serializers.HyperlinkedRelatedField(view_name="fleeksvideo:fleek-detail", read_only=True, lookup_field="slug")
    user = UserSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = SerializerMethodField()
    commentscount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Fleek
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'description',
            'videoUrl',
            'views',
            'musicCoverTitle',
            'likes',
            'publish',
            'commentscount',
            'comments',
        ]

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

    def get_commentscount(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        return c_qs.count()



class FleekListSerializer(serializers.HyperlinkedModelSerializer):
    #url = fleek_detail_url
    url = serializers.HyperlinkedRelatedField(view_name="fleeksvideo:fleek-detail", read_only=True, lookup_field="slug")
    likes = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    comments = SerializerMethodField()
    commentscount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Fleek
        fields = [
            'id',
            'url',
            'user',
            'slug',
            'title',
            'description',
            'publish',
            'videoUrl',
            'views',
            'musicCoverTitle',
            'likes',
            'commentscount',
            'comments'
        ]
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        print("comments number", c_qs.count())
        comments = CommentSerializer(c_qs, many=True).data
        return comments

    def get_commentscount(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        return c_qs.count()
    






def create_comment_serializer(model_type="fleek", slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp',
            ]
        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            print("its model_qs", model_qs)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=self.slug)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                    model_type, slug, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer



class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'timestamp',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='comments-api:thread')
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'url',
            'id',
            # 'content_type',
            # 'object_id',
            # 'parent',
            'content',
            'reply_count',
            'timestamp',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentChildSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]



class CommentDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    replies =   SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            #'content_type',
            #'object_id',
            'content',
            'reply_count',
            'replies',
            'timestamp',
            'content_object_url',
        ]
        read_only_fields = [
            #'content_type',
            #'object_id',
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0