from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.serializers import FeedPostSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id", 
            "email", 
            "username", 
            "full_name", 
            "is_verified", 
            "created_at", 
            "updated_at"
        )
        read_only_fields = (
            "id", 
            "email", 
            "is_verified", 
            "created_at", 
            "updated_at"
        )


class UserFeedSerializer(serializers.ModelSerializer):
    posts = FeedPostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("username", "posts")
