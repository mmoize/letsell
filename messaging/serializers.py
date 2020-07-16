from rest_framework import serializers
from authentication.models import User
from .models import Message


class MessageSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'subject', 'referenced_post', 'body', 'id']