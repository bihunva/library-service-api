from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from books.models import Book
from books.serializers import BookSerializer

from books.permissions import IsAdminOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    permission_classes = (IsAdminOrReadOnly,)

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]
