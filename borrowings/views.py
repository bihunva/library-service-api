from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowReturnSerializer,
    BorrowingCreateSerializer,
)
from payments.stripe import create_stripe_session


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BorrowingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book")
        is_active = self.request.query_params.get("is_active")

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if is_active is not None:
            match is_active:
                case "False":
                    queryset = queryset.filter(actual_return__isnull=False)
                case "True":
                    queryset = queryset.filter(actual_return__isnull=True)

        return queryset

    def get_serializer_class(self):
        if self.action == "return_borrow":
            return BorrowReturnSerializer
        if self.action == "create":
            return BorrowingCreateSerializer

        return BorrowingSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        borrowing = serializer.save()
        payment = create_stripe_session(borrowing, self.request)
        borrowing.payments.add(payment)
        borrowing.save()
        self.get_success_headers(serializer.data)
        return HttpResponseRedirect(payment.session_url)

    @action(methods=["POST"], detail=True, url_path="return")
    @transaction.atomic
    def return_borrow(self, request, pk=None):
        now = timezone.now()
        borrow = self.get_object()

        if borrow.actual_return is None:
            borrow.actual_return = now
            borrow.save()
            serializer = self.get_serializer(borrow, data=request.data)
            payment = borrow.payments.first()

            if serializer.is_valid():
                serializer.save()
                borrow.book.inventory += 1
                borrow.book.save()
                if payment.status == "PENDING" or (
                    payment.status == "PAID" and now > borrow.expected_return
                ):
                    payment = create_stripe_session(borrow, self.request)
                    return HttpResponseRedirect(payment.session_url)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": f"{borrow.user.email} already returned this borrow"},
            status=status.HTTP_400_BAD_REQUEST,
        )
