from core.config.settings import stripe
from core.apps.users.models import User


def get_or_create_stripe_customer(user: User) -> stripe.Customer:
    if user.stripe_id is None:
        stripe_customer = stripe.Customer.create(email=user.email)
        user.stripe_id = stripe_customer.id
        user.save()
        return stripe_customer
    else:
        return stripe.Customer.retrieve(user.stripe_id)
