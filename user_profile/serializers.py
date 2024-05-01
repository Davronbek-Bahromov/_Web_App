from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =  User
        fields = ['id', 'username', ]

class UserProfileSerializer(serializers.ModelSerializer):
    name = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['name', 'photo', 'bio', 'phone', 'follows', 'twitter_link', 'instagram_link', 'facebook_link', 'telegram_link', 'pinterest_link']