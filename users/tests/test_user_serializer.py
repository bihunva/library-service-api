from django.test import TestCase
from users.models import User
from users.serializers import UserSerializer


class TestUserSerializer(TestCase):
    def test_create_user(self):
        serializer = UserSerializer()
        data = {
            "email": "user@example.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
        }
        instance = serializer.create(data)

        self.assertIsInstance(instance, User)

        self.assertEqual(instance.email, "user@example.com")
        self.assertEqual(instance.first_name, "John")
        self.assertEqual(instance.last_name, "Doe")

        self.assertTrue(instance.check_password("password123"))

    def test_update_user(self):
        user = User.objects.create_user(
            email="user@example.com", password="testpassword"
        )
        serializer = UserSerializer(instance=user)
        data = {
            "email": "newuser@example.com",
            "first_name": "Jane",
            "last_name": "Doe",
            "password": "newpassword123",
        }
        instance = serializer.update(user, data)

        self.assertIsInstance(instance, User)

        self.assertEqual(instance.email, "newuser@example.com")
        self.assertEqual(instance.first_name, "Jane")
        self.assertEqual(instance.last_name, "Doe")

        self.assertTrue(instance.check_password("newpassword123"))
