from django.conf import settings
from django.db import models

from books.models import Book


class Borrowing(models.Model):
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    expected_return = models.DateTimeField()
    actual_return = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.book} borrowed by {self.user}"
