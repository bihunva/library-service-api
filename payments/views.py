import os
from datetime import datetime, timedelta

import stripe
from django.http import HttpResponseRedirect
from django.urls import reverse
from dotenv import load_dotenv
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentSerializer


load_dotenv()  # load variables from the .env file

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


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

    @action(methods=["GET"], detail=True, url_path="success")
    def success(self, request, pk):
        payment = Payment.objects.get(pk=pk)
        session_id = payment.session_id
        events = stripe.Event.list(type="checkout.session.completed")
        filtered_events = [
            event
            for event in events["data"]
            if event["data"]["object"]["id"] == session_id
            and event["type"] == "checkout.session.completed"
        ]
        if len(filtered_events) > 0:
            event_data = filtered_events[0]["data"]["object"]
            payment_status = event_data["payment_status"]
            if payment_status == "paid":
                payment.status = "PAID"
                payment.save()
                return HttpResponseRedirect(
                    reverse(
                        "payments:payment-detail", kwargs={"pk": payment.id}
                    )
                )
        return HttpResponseRedirect(payment.session_url)

    @action(detail=True, methods=['GET'], url_path='cancel')
    def cancel_payment(self, request, pk=None):
        payment = self.get_object()

        if payment.status == Payment.StatusChoices.PAID:
            return Response({"detail": "Payment has already been paid."}, status=status.HTTP_400_BAD_REQUEST)
        time_now = datetime.now()
        time_limit = time_now + timedelta(hours=24)
        message = f"Payment can be made until {time_limit.strftime('%Y-%m-%d %H:%M:%S')} (server time)."
        return Response({"detail": message})





