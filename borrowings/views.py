from rest_framework import viewsets, mixins

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Borrowing.objects.all()
        return Borrowing.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
