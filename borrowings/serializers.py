from rest_framework import serializers

from borrowings.models import Borrowing
from books.serializers import BookSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrowed_at",
            "expected_return",
            "actual_return",
            "is_active",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrowed_at",
            "expected_return",
            "actual_return",
        )
        # read_only_fields = ("id", "borrowed_at", "actual_return")

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


class BorrowReturnSerializer(BorrowingSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "actual_return")
