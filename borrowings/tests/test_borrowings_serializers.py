from books.models import Book
from borrowings.serializers import BorrowingCreateSerializer
from django.test import TestCase
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from users.models import User


class BorrowingCreateSerializerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="test@example.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        self.user2 = User.objects.create_user(
            email="test2@example.com",
            password="password",
            first_name="John",
            last_name="Doe",
        )
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=1, daily_fee=1.00
        )
        self.data = {
            "book": self.book.id,
            "expected_return": timezone.now() + timedelta(days=7),
        }

    def test_create_with_available_book(self):
        serializer = BorrowingCreateSerializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save(user=self.user1)

        # Verify that the borrowing was created with the expected data
        self.assertEqual(borrowing.book, self.book)
        self.assertEqual(borrowing.user, self.user1)
        self.assertEqual(borrowing.expected_return, self.data["expected_return"])
        self.assertEqual(borrowing.actual_return, None)

        # Verify that the book inventory was decreased by 1
        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 0)

    def test_create_with_unavailable_book(self):
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Cover.HARD,
            inventory=0,
            daily_fee=1.0,
        )
        data = {
            "book": book.id,
            "expected_return": "2023-05-01T00:00:00Z"
        }
        serializer = BorrowingCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Verify that the book inventory was not decreased
        book.refresh_from_db()
        self.assertEqual(book.inventory, 0)
