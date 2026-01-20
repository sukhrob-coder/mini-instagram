from django.contrib import admin

from .models import CommentLike, Post, PostComment, PostLike


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "created_at")
    list_filter = ("created_at",)
    search_fields = ("title", "content", "author__username")
    ordering = ("-created_at",)


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("content", "author__username")
    ordering = ("-created_at",)


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "created_at")
    list_filter = ("created_at",)
    ordering = ("-created_at",)


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "comment", "created_at")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
