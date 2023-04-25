import stripe
from django.conf import settings
from django.shortcuts import redirect
from requests import Response
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import PaymentSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = "http://localhost:4242"


class PaymentViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Payment.objects.select_related("borrowing")
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.is_staff:
            return self.queryset.filter(borrowing__user=user)

        return self.queryset

    @action(methods=["post"], detail=False)
    def stripe_session(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "currency": "usd",
                        "price": "{{BOOK_PRICE}}",
                        "quantity": 1,
                    },
                ],
                mode="payment",
                success_url=DOMAIN + "/success.html",
                cancel_url=DOMAIN + "/cancel.html",
            )
        except stripe.error.StripeError as e:
            return Response({"error": str(e)})

        return redirect(checkout_session.url, code=303)
