from datetime import date

import stripe

from django.conf import settings

from borrowings.models import Borrowing

stripe.api_key = settings.STRIPE_SECRET_KEY


def stripe_session(
        borrowing: Borrowing,
        url: str,
        start_date: date,
        end_date: date,
        is_ok: bool,
) -> stripe.checkout.Session:
    money_to_pay = (end_date - start_date).days * borrowing.book.daily_fee
    product = ""
    if is_ok:
        money_to_pay *= 2
        product = "free "

    url = url.rsplit("/", 2)[0] + "/borrowings/" + str(borrowing.id)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "amount": int(money_to_pay * 100),
                    "product_data": {
                        "name": product + str(borrowing),
                    },
                },
                "quantity":  1,
            },
        ],
        mode="payment",
        success_url=url + "/success?session_id={checkout_session.id}",
        cancel_url=url + "/cancel?session_id={checkout_session.id}",
    )

    return checkout_session
