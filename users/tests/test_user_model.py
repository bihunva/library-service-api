from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass",
            first_name="John",
            last_name="Doe",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNotNone(user.date_joined)
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpass")

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="testpass"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNotNone(admin_user.date_joined)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com", password="testpass", is_superuser=False
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com", password="testpass", is_staff=False
            )
