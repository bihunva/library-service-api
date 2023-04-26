import stripe

from django.urls import reverse
from django.utils import timezone
from django.conf import settings

from payments.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(borrowing, request):
    now = timezone.now()
    if now < borrowing.expected_return:
        type_payment = Payment.TypeChoices.PAYMENT
        money_to_pay = (
                               borrowing.expected_return - borrowing.borrowed_at
                       ).days * borrowing.book.daily_fee
    else:
        type_payment = Payment.TypeChoices.FINE
        money_to_pay = (
                (borrowing.actual_return - borrowing.expected_return).days
                * 2
                * borrowing.book.daily_fee
        )

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
        cancel_url=url + "cancel?session_id={checkout_session.id}",
    )

    payment.session_url = session.url
    payment.session_id = session.id
    payment.save()

    return payment
