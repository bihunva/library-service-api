import os
import stripe

from _decimal import Decimal, ROUND_HALF_UP
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from dotenv import load_dotenv
from books.models import Book
from borrowings.models import Borrowing
from payments.models import Payment
from payments.stripe import create_stripe_session


User = get_user_model()
load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaymentUtilsTests(TestCase):
    def setUp(self):
        self.borrowed_at = timezone.now()
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="hard",
            inventory=10,
            daily_fee=1.99
        )
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return=self.borrowed_at + timezone.timedelta(days=7)
        )
        self.factory = RequestFactory()
        self.request = self.factory.get(reverse("payments:payment-detail", kwargs={"pk": 1}))

    def test_create_stripe_session(self):
        payment = create_stripe_session(self.borrowing, self.request)
        self.assertIsNotNone(payment)

        payment = Payment.objects.filter(borrowing=self.borrowing).first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.status, Payment.StatusChoices.PENDING)
        self.assertEqual(payment.type, Payment.TypeChoices.PAYMENT)
        self.assertEqual(payment.money_to_pay.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
                         Decimal((
                                             self.borrowing.expected_return - self.borrowing.borrowed_at).days * self.book.daily_fee).quantize(
                             Decimal("0.01"), rounding=ROUND_HALF_UP))

        self.assertIsNotNone(payment.session_url)
        self.assertIsNotNone(payment.session_id)
