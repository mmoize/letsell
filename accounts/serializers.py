from rest_framework import serializers
from authentication.models import User
from .models import Profile


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
        fields = ('user_id','username',  'first_name', 'last_name', 'country', 'city', 'bio', 'image', 'user')
    
