from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.serializers import Base64ImageField

from .models import Post, PostComment, PostLike

User = get_user_model()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ("id", "author", "post", "created_at")
        read_only_fields = ("id", "author", "post", "created_at")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = PostComment
        fields = ("id", "author", "content", "created_at")
        read_only_fields = ("id", "author", "created_at")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    image = Base64ImageField()
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "image",
            "title",
            "content",
            "created_at",
            "likes_count",
            "comments_count",
            "is_liked",
        )
        read_only_fields = (
            "id",
            "author",
            "created_at",
            "likes_count",
            "comments_count",
            "is_liked",
        )

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.likes.filter(author=user).exists()
        return False


class FeedPostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "title", "content", "likes")

    def get_likes(self, obj):
        return obj.likes.values_list("author_id", flat=True)
