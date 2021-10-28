from rest_framework.response import Response
from rest_framework import status, views, viewsets, permissions

from core.apps.users.models import User
from core.apps.payments.models import CurrentPaymentPlan, PaymentPlanIntent
from core.apps.payments.serializers import (
    PaymentPlanIntentSerializer,
    PaymentPlanSerializer,
)
from core.config.settings import STRIPE_WEBHOOK_SECRET, stripe


class PaymentPlanIntentViewset(viewsets.GenericViewSet):

    serializer_class = PaymentPlanIntentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user: User = request.user
        plan_type = request.data.get("plan_type")
        if plan_type is None:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        payment_plan_intent = PaymentPlanIntent.objects.from_plan_type(
            user=user, plan_type=plan_type,
        )
        serializer = self.get_serializer(instance=payment_plan_intent)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CurrentPaymentPlanViewSet(viewsets.GenericViewSet):

    serializer_class = PaymentPlanSerializer
    permission_classes = (permissions.IsAuthenticated,)

    SUCCESSFUL_PAYMENT_INTENT = "succeeded"

    def create(self, request, format=None):
        # TODO: check to see if this is an existing cancelled plan.
        # right now we will double charge users if they cancel and then upgrade again
        user: User = request.user
        if user.is_anonymous or not user.is_authenticated:
            return Response(
                data={"details": "unknown user"}, status=status.HTTP_403_FORBIDDEN
            )
        intent_data = request.data.get("plan_payment_intent", dict())
        intent_id = int(intent_data.get("id"))
        try:
            intent = PaymentPlanIntent.objects.get(pk=intent_id)
            if intent.stripe_id != intent_data.get("stripe_id"):
                raise ValueError("could not find payment intent")
            if intent.client_secret != intent_data.get("client_secret"):
                raise ValueError("could not find payment intent")
        except (PaymentPlanIntent.DoesNotExist, ValueError):
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
        stripe_intent = stripe.PaymentIntent.retrieve(intent.stripe_id)
        if stripe_intent.status == self.SUCCESSFUL_PAYMENT_INTENT:
            payment_plan = CurrentPaymentPlan.objects.create_or_update(
                user=user,
                plan_type=intent.plan_type,
                subscription_id=intent.subscription_id,
            )
            plan_serializer = self.get_serializer(instance=payment_plan)
            intent.delete()
            return Response(data=plan_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user: User = request.user
        payment_plan = CurrentPaymentPlan.objects.get(user=user)
        if payment_plan.subscription_id is not None:
            stripe.Subscription.modify(
                sid=payment_plan.subscription_id, cancel_at_period_end=True
            )
        payment_plan.is_cancelled = True
        payment_plan.save()
        plan_serializer = self.get_serializer(instance=payment_plan)
        return Response(data=plan_serializer.data, status=status.HTTP_200_OK)


# TODO: successful subscription payment method
class StripeWebhookAPIView(views.APIView):

    CREATED_SUBSCRIPTION_EVENT = "customer.subscription.created"
    UPDATED_SUBSCRIPTION_EVENT = "customer.subscription.updated"
    DELETED_SUBSCRIPTION_EVENT = "customer.subscription.deleted"
    INVOICE_PAYMENT_SUCCEEDED = "invoice.payment_succeeded"

    def get_event_type_and_data(self, request, stripe_signatures):
        if not self.WEBHOOK_SECRET:
            raise ValueError("Stripe webhook secret not set")
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body,
                sig_header=stripe_signatures,
                secret=STRIPE_WEBHOOK_SECRET,
            )
            data = event["data"]
        except Exception as e:
            raise e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event["type"]
        return event_type, data

    def post(self, request, format=None):
        event_type, event_data = self.get_event_type_and_data(
            request, request.headers.get("Stripe-Signature")
        )
        if event_type == self.CREATED_SUBSCRIPTION_EVENT:
            pass  # TODO - move logic to handle through here
        elif event_type == self.UPDATED_SUBSCRIPTION_EVENT:
            pass  # TODO - move logic to handle through here
        elif event_type == self.DELETED_SUBSCRIPTION_EVENT:
            pass  # TODO - move logic to handle through here
        elif event_type == self.INVOICE_PAYMENT_SUCCEEDED:
            data_object = event_data["object"]
            if data_object["billing_reason"] == "subscription_create":
                subscription_id = data_object["subscription"]
                payment_intent_id = data_object["payment_intent"]

                # Retrieve the payment intent used to pay the subscription
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

                # Set the default payment method
                stripe.Subscription.modify(
                    subscription_id,
                    default_payment_method=payment_intent.payment_method,
                )
        return Response(data=None, status=status.HTTP_200_OK)
