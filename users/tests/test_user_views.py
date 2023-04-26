from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.authentication import JWTAuthentication


class ManageUserViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.url = "/api/users/me/"
        self.auth = JWTAuthentication()

    def test_get_object(self):
        self.client.force_authenticate(self.user, token=self.auth)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_object(self):
        self.client.force_authenticate(self.user, token=self.auth)
        response = self.client.put(
            self.url,
            {
                "email": "new-email@example.com",
                "password": "newpassword",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "new-email@example.com")
        self.assertTrue(self.user.check_password("newpassword"))
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
