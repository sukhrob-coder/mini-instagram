from django.urls import path

from .views import (CommentDetailView, PostCommentListView, PostDetailView, PostLikeView, PostListCreateView)

urlpatterns = [
    path("posts/", PostListCreateView.as_view(), name="post-list-create"),
    path("posts/<uuid:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<uuid:pk>/like/", PostLikeView.as_view(), name="post-like"),
    path(
        "posts/<uuid:pk>/comments/", PostCommentListView.as_view(), name="post-comments"
    ),
    path(
        "posts/<uuid:post_id>/comments/<uuid:comment_id>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
    
]
