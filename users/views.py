from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from rest_framework import generics, permissions

from common.paginations import CustomPageNumberPagination

from posts.models import Post

from .serializers import UserSerializer, UserFeedSerializer

User = get_user_model()


class UserMeView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserFeedView(generics.ListAPIView):
    queryset = (
        User.objects.filter(posts__isnull=False)
        .prefetch_related(
            Prefetch(
                "posts",
                queryset=Post.objects.all().prefetch_related("likes")
            )
        )
        .distinct()
        .order_by("-created_at")
    )
    serializer_class = UserFeedSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPageNumberPagination
