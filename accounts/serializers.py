from rest_framework import serializers
from authentication.models import User


from .models import Profile, FollowerRelationship




class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    user_id = serializers.CharField(source='user.id')
    first_name = serializers.CharField(allow_blank=False, required=True)
    last_name = serializers.CharField(allow_blank=False, required=True)
    country = serializers.CharField(allow_blank=True, required=False)
    city = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)



    class Meta:
        model = Profile
        fields = ('user_id','username',
                  'first_name', 'last_name',
                  'country', 'city',
                  'bio', 'image',
                  'user',
                 )




# class ProfileDetailSerializer(serializers.HyperlinkedModelSerializer):
#     first_name = serializers.CharField(allow_blank=False, required=True)
#     last_name = serializers.CharField(allow_blank=False, required=True)
#     country = serializers.CharField(allow_blank=True, required=False)
#     city = serializers.CharField(allow_blank=True, required=False)
#     bio = serializers.CharField(allow_blank=True, required=False)
#     follower_count = serializers.SerializerMethodField(read_only=True)
#     following_count = serializers.SerializerMethodField(read_only=True)
#     is_following = serializers.SerializerMethodField(read_only=True)
#     followin = FollowerRelationshipSerializer(read_only=True, many=True)

#     class Meta:
#         model = Profile
#         fields = (
#                   'first_name', 'last_name',
#                   'country', 'city',
#                   'bio', 'image',
#                   'user', 'follower_count', 
#                   'following_count', 'is_following',
#                    )

#     def get_is_following(self, obj):
#         # request???
#         is_following = False
#         context = self.context
#         request = context.get("request")
#         if request:
#             user = request.user
#             is_following = user in obj.followers.all()
#         return is_following
    
#     def get_following_count(self, obj):
#         return obj.user.following.count()

#     # def get_following(self, obj):
#     #     return obj.user.following.all()
    
#     def get_follower_count(self, obj):
#         return obj.followers.count()