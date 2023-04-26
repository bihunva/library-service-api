from django.urls import path, include
from rest_framework.routers import DefaultRouter

from borrowings.views import BorrowingViewSet

router = DefaultRouter()
router.register("", BorrowingViewSet, basename="borrowings")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "borrowings/<int:pk>/return/",
        BorrowingViewSet.as_view({"post": "return_borrow"}),
        name="return_borrow",
    ),
]

app_name = "borrowings"
