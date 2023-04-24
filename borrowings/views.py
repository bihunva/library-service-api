import datetime

from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer, BorrowReturnSerializer


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Borrowing.objects.all().select_related("book")
        return Borrowing.objects.filter(user=self.request.user.id).select_related(
            "book"
        )

    def get_serializer_class(self):
        if self.action == "return_borrow":
            return BorrowReturnSerializer
        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="return")
    @transaction.atomic
    def return_borrow(self, request, pk=None):
        borrow = self.get_object()
        serializer = self.get_serializer(borrow, data=request.data)

        if borrow.actual_return is None:
            if serializer.is_valid():
                serializer.save()
                borrow.book.inventory += 1
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": f"{borrow.user.email} already returned this borrow"},
            status=status.HTTP_400_BAD_REQUEST,
        )
