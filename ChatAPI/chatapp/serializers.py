from rest_framework import serializers
from .models import User,Chat

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'password', 'tokens')
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id','user', 'message', 'response', 'timestamp')
        read_only_fields = ('user', 'response', 'timestamp')
