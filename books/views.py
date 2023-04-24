from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from books.models import Book
from books.serializers import BookSerializer

from books.permissions import IsAdminOrReadOnly


class BookViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = (IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]
