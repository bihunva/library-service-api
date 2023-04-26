from books.models import Book
from borrowings.models import Borrowing
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import timedelta
from django.utils import timezone
from users.models import User


class BorrowingViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create a user
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword"
        )

        # create a book
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", inventory=2, daily_fee=0.5
        )

        # create a borrowing
        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return=timezone.now() + timedelta(days=7),
        )

    def test_return_borrow(self):
        # login the user
        self.client.force_authenticate(user=self.user)

        # call the return_borrow API endpoint
        url = reverse("borrowings:return_borrow", args=[self.borrowing.pk])
        response = self.client.post(url, format="json")

        # assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the borrowing's actual_return is set to the current time
        borrowing = Borrowing.objects.get(pk=self.borrowing.pk)
        self.assertIsNotNone(borrowing.actual_return)

        # assert that the book's inventory is incremented
        book = Book.objects.get(pk=self.book.pk)
        self.assertEqual(book.inventory, 3)
