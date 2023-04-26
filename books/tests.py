from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .serializers import BookSerializer

from django.contrib.auth import get_user_model

from books.models import Book


BOOK_URL = reverse("books:book-list")


def detail_url(book_id: int):
    return reverse("books:book-detail", args=[book_id])


def sample_book(**params):
    defaults = {
        "title":"The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "cover": "Book.Cover.HARD",
        "inventory": 10,
        "daily_fee": 2.50
    }

    defaults.update(params)

    return Book.objects.create(**defaults)


class UnAuthenticatedBookApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_book_list(self):
        response = self.client.get(BOOK_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class AuthenticatedBookApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "regularuser@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()

    def test_get_book_detail(self):
        url = detail_url(self.book.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book_data = response.data
        serializer = BookSerializer(self.book)
        self.assertEqual(book_data, serializer.data)


class AdminBookApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "regularuser@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.book = sample_book()

    def test_create_book(self):
        payload = {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "cover": Book.Cover.SOFT,
            "inventory": 5,
            "daily_fee": "3.00",
        }

        result = self.client.post(BOOK_URL, payload)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        url = detail_url(self.book.id)
        data = {
            "title": "The Great Gatsby (Updated)",
            "author": "F. Scott Fitzgerald (Updated)",
            "cover": Book.Cover.SOFT,
            "inventory": 15,
            "daily_fee": 3.00,
        }

        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


