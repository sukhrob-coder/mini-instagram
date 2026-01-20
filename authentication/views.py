from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

from common.utils import get_verification_token

from .serializers import EmailVerificationSerializer, LoginSerializer, RegisterSerializer

User = get_user_model()


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {
                "access": serializer.validated_data["tokens"]["access"],
                "refresh": serializer.validated_data["tokens"]["refresh"],
            },
            status=status.HTTP_200_OK,
        )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_verified=False)

        token = get_verification_token(user)

        headers = self.get_success_headers(serializer.data)

        return Response(
            {"verification_token": token},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class VerifyEmailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():

            token_str = serializer.validated_data["token"]

            try:
                token = AccessToken(token_str)

                if token.get("type") != "email_verification":
                    return Response(
                        {"error": "Invalid token type"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user_id = token["user_id"]
                user = User.objects.get(id=user_id)

                if user.is_verified:
                    return Response(
                        {"message": "Email already verified"}, status=status.HTTP_200_OK
                    )

                user.is_verified = True

                user.save()
                return Response(
                    {"message": "Email successfully verified"},
                    status=status.HTTP_200_OK,
                )

            except TokenError:
                return Response(
                    {"error": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CleanupUnverifiedUsersView(APIView):
    permission_classes = (IsAdminUser,)

    def delete(self, request):
        threshold = timezone.now() - timedelta(hours=24)
        deleted_count, _ = User.objects.filter(
            is_verified=False, date_joined__lt=threshold
        ).delete()
        return Response(
            {"message": f"Deleted {deleted_count} unverified users"},
            status=status.HTTP_200_OK,
        )
