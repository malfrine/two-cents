from datetime import datetime, time, timedelta
from typing import Optional, Union

from django.db import models
from django.utils import timezone
from core.apps.payments.utilities import get_or_create_stripe_customer

from core.apps.users.models import User as AuthUser
from core.config.settings import IS_STRIPE_TEST, stripe


class PlanType(models.TextChoices):
    LIMITED_FREE = "free", "Limited Free Forever Plan"
    ONE_TIME = "one-time", "One-Time Fee Plan"
    MONTHLY = "monthly", "Monthly Subscription Plan"
    ANNUAL = "annual", "Annual Subscription Plan"
    UNLIMITED_FREE = "unlimited-free" "Unlimited Free Plan"


def get_price_id(plan_type: PlanType):
    if IS_STRIPE_TEST:
        map_ = {
            PlanType.ONE_TIME: "price_1Jem3MIV4zbGa3wDs1ZvkoT5",
            PlanType.MONTHLY: "price_1Jelq5IV4zbGa3wDAZZTXuVd",
            PlanType.ANNUAL: "price_1Jem3xIV4zbGa3wDnNzWqxFq",
        }
    else:
        map_ = {
            PlanType.ONE_TIME: "price_1JqOF4IV4zbGa3wD4SqDMB4Z",
            PlanType.MONTHLY: "price_1JqOFWIV4zbGa3wD9Dczw84H",
            PlanType.ANNUAL: "price_1JqOG0IV4zbGa3wD9U9xGibJ",
        }
    return map_.get(plan_type)


class PaymentPlanIntentManager(models.Manager):
    def from_plan_type(
        self,
        user: AuthUser,
        plan_type: Union[PlanType, str],
        promotion_code: Optional[str] = None,
    ):
        if isinstance(plan_type, str):
            plan_type = PlanType(plan_type)
        stripe_customer = get_or_create_stripe_customer(user)
        price_id = get_price_id(plan_type)
        price = stripe.Price.retrieve(price_id)
        if price.recurring:
            subscription = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=[{"price": price_id,}],  # noqa: E231
                payment_behavior="default_incomplete",
                expand=["latest_invoice.payment_intent"],
                promotion_code=promotion_code,
            )
            payment_intent = subscription.latest_invoice.payment_intent
            subscription_id = subscription.id
        else:
            payment_intent = stripe.PaymentIntent.create(
                amount=price.unit_amount,
                currency=price.currency,
                customer=stripe_customer.id,
                promotion_code=promotion_code,
            )
            subscription_id = None

        payment_plan_intent = self.create(
            user=user,
            plan_type=plan_type,
            stripe_id=payment_intent.id,
            client_secret=payment_intent.client_secret,
            created_dt=timezone.now(),
            subscription_id=subscription_id,
        )
        payment_plan_intent.save()
        return payment_plan_intent


class PaymentPlanIntent(models.Model):
    user = models.ForeignKey(
        AuthUser, on_delete=models.CASCADE, related_name="payment_plan_intentions"
    )
    created_dt = models.DateTimeField(verbose_name="Created Datetime")
    plan_type = models.CharField(max_length=50, choices=PlanType.choices)
    stripe_id = models.CharField(
        verbose_name="Stripe Payment Intent ID", max_length=225
    )
    client_secret = models.CharField(verbose_name="Client Secret", max_length=225)
    subscription_id = models.CharField(
        max_length=50, null=True, default=None, blank=True
    )

    objects = PaymentPlanIntentManager()


class CurrentPaymentPlanManager(models.Manager):
    def create_or_update(
        self, user: AuthUser, plan_type: PlanType, subscription_id: str
    ):
        try:
            payment_plan = self.get(user=user)
            payment_plan.plan_type = plan_type
            payment_plan.payment_dt = timezone.now()
            payment_plan.subscription_id = subscription_id
            payment_plan.is_cancelled = False
        except CurrentPaymentPlan.DoesNotExist:
            payment_plan = self.model(
                user=user,
                plan_type=plan_type,
                payment_dt=timezone.now(),
                subscription_id=subscription_id,
            )
        payment_plan.save()
        return payment_plan

    def create_default(self, user: AuthUser):
        self.create_or_update(user, PlanType.LIMITED_FREE, None)


# TODO: rename to PremiumPlan
class CurrentPaymentPlan(models.Model):
    user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, related_name="payment_plan"
    )
    plan_type = models.CharField(
        max_length=50, choices=PlanType.choices, default=PlanType.LIMITED_FREE
    )
    payment_dt = models.DateTimeField(verbose_name="Payment Datetime")
    subscription_id = models.CharField(
        max_length=50, null=True, default=None, blank=True
    )
    is_cancelled = models.BooleanField(verbose_name="Is Plan Cancelled", default=False)

    @property
    def expiration_dt(self):
        duration_days_map = {"one-time": 1, "monthly": 30, "annual": 365}
        duration_days = duration_days_map.get(self.plan_type)
        if duration_days is None:
            expiration_date = datetime.max
        else:
            expiration_date = (self.payment_dt + timedelta(days=duration_days)).date()
        return datetime.combine(expiration_date, time.max)

    @property
    def is_free_plan(self):
        return self.plan_type in (PlanType.LIMITED_FREE, PlanType.UNLIMITED_FREE)

    @property
    def is_premium_plan(self):
        return self.plan_type in (
            PlanType.ONE_TIME,
            PlanType.UNLIMITED_FREE,
            PlanType.MONTHLY,
            PlanType.ANNUAL,
        )

    @property
    def is_subscription_plan(self):
        return self.plan_type in (PlanType.MONTHLY, PlanType.ANNUAL)

    @property
    def verbose_plan_type(self):
        return self.plan_type

    objects = CurrentPaymentPlanManager()

    def __str__(self) -> str:
        return f"{self.user.email}'s payment plan ({self.id})"
