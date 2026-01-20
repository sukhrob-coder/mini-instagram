from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("auth-register")
        self.login_url = reverse("auth-login")
        self.verify_url = reverse("auth-verify-email")
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "TestPassword123!",
            "password_confirm": "TestPassword123!",
        }

    def test_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("verification_token", response.data)
        self.assertTrue(User.objects.filter(email=self.user_data["email"]).exists())

    def test_registration_duplicate_email(self):
        self.client.post(self.register_url, self.user_data)

        duplicate_data = self.user_data.copy()
        duplicate_data["username"] = "differentuser"
        response = self.client.post(self.register_url, duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_registration_duplicate_username(self):
        self.client.post(self.register_url, self.user_data)

        duplicate_data = self.user_data.copy()
        duplicate_data["email"] = "different@example.com"
        response = self.client.post(self.register_url, duplicate_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_login_success(self):
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(email=self.user_data["email"])
        user.is_verified = True
        user.save()

        login_data = {
            "email_or_username": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_protected_endpoint_access(self):
        self.client.post(self.register_url, self.user_data)
        user = User.objects.get(email=self.user_data["email"])
        user.is_verified = True
        user.save()

        login_data = {
            "email_or_username": self.user_data["email"],
            "password": self.user_data["password"],
        }
        login_response = self.client.post(self.login_url, login_data)
        token = login_response.data["access"]

        post_url = reverse("post-list-create")

        response = self.client.post(
            post_url, {"title": "Test Post", "content": "Content"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        post_data = {
            "title": "Valid Post Title",
            "content": "Valid Content",
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
        }
        response = self.client.post(post_url, post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token")
        response = self.client.post(post_url, post_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
