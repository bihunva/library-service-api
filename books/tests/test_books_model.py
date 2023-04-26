from books.models import Book
from django.test import TestCase


class BookModelTest(TestCase):
    def test_book_str(self):
        book = Book.objects.create(
            title="To Kill a Mockingbird",
            author="Harper Lee",
            cover=Book.Cover.SOFT,
            inventory=5,
            daily_fee=1.99,
        )
        self.assertEqual(str(book), "To Kill a Mockingbird by Harper Lee")
