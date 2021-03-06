from rest_framework import serializers
from authentication.models import User
from authentication.serializers import UserSerializer
from discover.models import Post

from accounts.models import Profile, FollowerRelationship
import datetime
# class FollowerRelationship(serializers.HyperlinkedModelSerializer):
class FollowerRelationshipSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FollowerRelationship
        fields = ('following','follower', 'when_follwed');

class ProfileDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(allow_blank=False, required=True)
    last_name = serializers.CharField(allow_blank=False, required=True)
    country = serializers.CharField(allow_blank=True, required=False)
    city = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    lastRefresh = serializers.SerializerMethodField(read_only=True)



    class Meta:
        model = Profile
        fields = (
                  'first_name', 'last_name',
                  'country', 'city',
                  'bio', 'image',
                  'user', 'follower_count', 
                  'following_count', 'is_following','lastRefresh'
                   )



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(source='user.username')
    user_id = serializers.CharField(source='user.id')
    first_name = serializers.CharField(allow_blank=False, required=True)
    last_name = serializers.CharField(allow_blank=False, required=True)
    country = serializers.CharField(allow_blank=True, required=False)
    city = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    followers = UserSerializer(read_only=True, many=True)
    user = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True, many=True)
    lastRefresh = serializers.SerializerMethodField(read_only=True)
    posts_count = serializers.SerializerMethodField(read_only=True)



    class Meta:
        model = Profile
        fields = ('user_id','username',
                  'first_name', 'last_name',
                  'country', 'city',
                  'bio', 'image',
                  'user', 'follower_count', 
                  'following_count', 'is_following',
                  'followers', 'following','lastRefresh','posts_count'
                 )

    def get_is_following(self, obj):
    
        is_following = False
        context = self.context
        request = context.get("request")
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following


    # def get_following(self, obj):
    #     context = self.context
    #     request = context.get("request")
    #     if request:
    #         user = request.user.username
    #         profile_obj = Profile.objects.filter(user__username=user)
    #         print('data ', obj.user.following.all())
    #     return obj.user.following.all()
    
    def get_following_count(self, obj):
        return obj.user.following.count()


    # def get_following(self, obj):
    #     my_following = obj.user.following.all()
    #     following = my_following
    #     print('this is followers 1', following.all())
    #     return following


    # def get_following(self, obj):
    #     request = context.get("request")
    #     user = request.user.username
    #     profile_obj =  Profile.objects.filter(user__username=user)
    #     return profile_obj.following.all()
    
    def get_follower_count(self, obj):
        my_following = obj.user.following.all()
        following = my_following

        print('this is followers 2', following)

        return obj.followers.count()

    def get_lastRefresh (self, obj):

        time = datetime.datetime.now()

        return time

    def get_posts_count(self, obj):
        req = obj.user_id
        posts = Post.objects.filter(owner_id = obj.user_id).count()
        return posts

    