import stripe
import os

from django.urls import reverse
from django.utils import timezone

from payments.models import Payment

from dotenv import load_dotenv

load_dotenv()  # load variables from the .env file

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
FINE_MULTIPLAYER = 2


def create_stripe_session(borrowing, request):
    now = timezone.now()
    if now < borrowing.expected_return:
        type_payment = Payment.TypeChoices.PAYMENT
        money_to_pay = (
            borrowing.expected_return - borrowing.borrowed_at
        ).days * borrowing.book.daily_fee
    else:
        type_payment = Payment.TypeChoices.FINE
        money_pending = 0
        print(borrowing.payments.all())
        payment_expired = borrowing.payments.first()
        if payment_expired.status == "PENDING":
            money_pending = (
                borrowing.expected_return - borrowing.borrowed_at
            ).days * borrowing.book.daily_fee
            print(money_pending)

        money_to_pay = (
            (borrowing.actual_return - borrowing.expected_return).days
            * FINE_MULTIPLAYER
            * borrowing.book.daily_fee
        ) + money_pending
        payment_expired.delete()
        print(money_pending)

    stripe_unit_amount = int(money_to_pay * 100)
    price = stripe.Price.create(
        unit_amount=stripe_unit_amount,
        currency="usd",
        product_data={
            "name": borrowing.book.title,
        },
    )
    payment = Payment(
        status=Payment.StatusChoices.PENDING,
        type=type_payment,
        borrowing=borrowing,
        money_to_pay=money_to_pay,
    )
    payment.save()
    url = request.build_absolute_uri(
        reverse("payments:payment-detail", kwargs={"pk": payment.id})
    )
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price.id,
                "quantity": 1,
            },
        ],
        payment_intent_data={
            "metadata": {
                "borrowing_id": borrowing.id,
            },
        },
        mode="payment",
        success_url=url + "success/",
        cancel_url=url + "cancel/",
    )

    payment.session_url = session.url
    payment.session_id = session.id
    payment.save()

    return payment
