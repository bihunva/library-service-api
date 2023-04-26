import stripe
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from config import settings

from payments.models import Payment
from payments.serializers import PaymentSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY


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
        stripe.api_key = settings.STRIPE_SECRET_KEY
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
