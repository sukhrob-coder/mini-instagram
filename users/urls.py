from django.urls import path

from .views import UserFeedView, UserMeView

urlpatterns = [
    path("me/", UserMeView.as_view(), name="user-me"),
    path("feed/", UserFeedView.as_view(), name="user-feed"),
]
