from django.test import TestCase
from django.utils import timezone

from books.models import Book
from borrowings.models import Borrowing
from users.models import User


class BorrowingTestCase(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=1, daily_fee=1.00
        )
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        self.borrowing = Borrowing.objects.create(
            book=self.book, user=self.user, expected_return=timezone.now()
        )

    def test_is_active(self):
        self.assertTrue(self.borrowing.is_active)
        self.borrowing.actual_return = timezone.now()
        self.assertFalse(self.borrowing.is_active)

    def test_str(self):
        expected_string = f"{self.book} borrowed by {self.user}"
        self.assertEqual(str(self.borrowing), expected_string)
