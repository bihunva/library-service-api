from books.models import Book
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User


class BookViewPermissionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.admin_user)
        self.book = Book.objects.create(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            cover=Book.Cover.SOFT,
            inventory=5,
            daily_fee=1.99,
        )

    def test_list_books_permissions(self):
        user = User.objects.create_user(
            email="user@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=user)

        response = self.client.get("/api/books/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_book_permissions(self):
        response = self.client.post(
            "/api/books/",
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "cover": Book.Cover.HARD,
                "inventory": 10,
                "daily_fee": 2.99,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_book_permissions(self):
        updated_book_data = {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee (updated)",
            "cover": Book.Cover.SOFT,
            "inventory": 5,
            "daily_fee": 1.99,
        }

        response = self.client.put(f"/api/books/{self.book.id}/", updated_book_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_book_permissions(self):
        response = self.client.delete(f"/api/books/{self.book.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_admin_user_permissions(self):
        user = User.objects.create_user(
            email="user@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=user)

        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            "/api/books/",
            {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "cover": Book.Cover.HARD,
                "inventory": 10,
                "daily_fee": 2.99,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(
            f"/api/books/{self.book.id}/",
            {
                "title": "The Great Gatsby Revised Edition",
                "author": "F. Scott Fitzgerald",
                "cover": Book.Cover.SOFT,
                "inventory": 10,
                "daily_fee": 2.99,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(f"/api/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
