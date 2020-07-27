from rest_framework import serializers
from authentication.models import User
from .models import Message, Room
from authentication.serializers import UserSerializer
from discover.models import Post
from rest_framework.exceptions import NotAcceptable
from discover.serializers import PostSerializer


class GetUserMixin:
    def get_user_from_request(self):
        request = self.context.get('request')
        if not request:
            return None
        if not hasattr(request, 'user'):
            return None
        return request.user


class MessageSerializers(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['sender', 'recipient',  'referenced_post', 'body', 'id']

class MessagingSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    # sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'message', 'created', 'referenced_post']

class RoomSerializer(GetUserMixin, serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Room
        fields = ('id', 'title', 'participants')

    def validate_participants(self, value):
        user = self.get_user_from_request()
        if not user:
            return value

        if user not in value:
            raise serializers.ValidationError('User must be in participants.')
        return value


class MessagySerializer(GetUserMixin, serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all(), write_only=True)

    class Meta:
        model = Message
        fields = ('id', 'content', 'sender', 'room', 'created_at')

    def validate_sender(self, value):
        user = self.get_user_from_request()
        if not user:
            return value

        if user.id != value.id:
            raise serializers.ValidationError('User must be same with sender.')
        return value

    def validate_room(self, value):
        user = self.get_user_from_request()
        if not user:
            return value

        if not user.room_set.filter(id=value.id):
            raise serializers.ValidationError('User must be in room.')

        url_room_pk = self.context.get('view').kwargs.get('parent_lookup_room')
        if int(url_room_pk) != value.id:
            raise serializers.ValidationError('Room must be same with room of url.')
        return value


class LobbySerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Room
        fields = ('title', 'id', 'members')

class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'title')

class RooomSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ('id', 'message', 'sender')





class RoomxSerializer(serializers.HyperlinkedModelSerializer):        
    createdBy = UserSerializer(read_only=True) 
    url = serializers.HyperlinkedRelatedField(view_name="chat:room-detail", read_only=True, lookup_field="room")
 
    class Meta:
        model = Room
        fields = ['url','title','createdBy']

class MessagexSerializer(serializers.HyperlinkedModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    referenced_post_set  = PostSerializer(read_only=True)
    room_set =RoomxSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'message', 'recipient', 'room_set', 'sender', 'referenced_post_set', 'created')
    
    
    def create(self, validated_data):

        data = self.context['message_info']
        recipient_id = data['recipient']
        ref_post = data['referenced_post']
        post_ref = Post.objects.get(id=ref_post)
        print('this is rooms members ref', ref_post)
        members_recipient = User.objects.get(id=recipient_id)

        members_creater = self.context['request'].user.id

        room_obj= Room.objects.get_or_create(
            # id = data['id'],
            # title=data['title'],
            # members = recipient_id, members_creater

        )
        room_obj[0].members.add(recipient_id)
        room_obj[0].members.add(members_creater)
        room_instance = room_obj[0]
        print('this is room', )

        

        message_obj = Message.objects.create(
            sender = self.context['request'].user,
            recipient = members_recipient,
            referenced_post = post_ref,
            message = validated_data['message'],
            room = room_instance
        )

        
        return message_obj   
        



        



