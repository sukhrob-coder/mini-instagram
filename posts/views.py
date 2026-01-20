from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.paginations import CustomPageNumberPagination
from common.permissions import IsAuthor, IsAuthorOrReadOnly, IsVerified, IsVerifiedOrReadOnly

from .models import Post, PostComment, PostLike
from .serializers import CommentSerializer, PostSerializer


User = get_user_model()


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsVerifiedOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("title", "content")

    def get_queryset(self):
        queryset = Post.objects.all().select_related("author").order_by("-created_at")

        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class PostLikeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if post.author == user:
            return Response(
                {"error": "You cannot like your own post"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if PostLike.objects.filter(author=user, post=post).exists():
            return Response(
                {"message": "You already liked this post"}, status=status.HTTP_200_OK
            )

        PostLike.objects.create(author=user, post=post)
        return Response({"message": "Post liked"}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        PostLike.objects.filter(author=user, post=post).delete()
        return Response({"message": "Unliked"}, status=status.HTTP_204_NO_CONTENT)


class PostCommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsVerifiedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("pk")
        return PostComment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(generics.DestroyAPIView):
    queryset = PostComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthor, IsVerified)
    lookup_url_kwarg = "comment_id"


