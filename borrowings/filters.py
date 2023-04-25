import django_filters

from .models import Borrowing


class BorrowingFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter(field_name='actual_return',
                                             lookup_expr='isnull')

    class Meta:
        model = Borrowing
        fields = [
            'is_active',
        ]
