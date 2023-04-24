# serializers.py

from books.serializers import BookSerializer
from rest_framework import serializers

from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date"
        )

    def create(self, validated_data):
        book = validated_data.get("book")
        if book.inventory <= 0:
            raise serializers.ValidationError(
                {"error": "Book is out of stock."}
            )
        borrowing = Borrowing.objects.create(**validated_data)
        book.inventory -= 1
        book.save()

        return borrowing
