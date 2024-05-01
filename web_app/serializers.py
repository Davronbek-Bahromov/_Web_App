# from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import Post, Comment, Channel
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]
        
class ChannelSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta():
        model = Channel
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

class ReadOnlyPostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    channel = ChannelSerializer(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'created_by', 'post', 'body']