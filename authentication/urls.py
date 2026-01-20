from django.urls import path

from .views import CleanupUnverifiedUsersView, LoginView, RegisterView, VerifyEmailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("verify-email/", VerifyEmailView.as_view(), name="auth-verify-email"),
    path("cleanup/", CleanupUnverifiedUsersView.as_view(), name="auth-cleanup"),
]
