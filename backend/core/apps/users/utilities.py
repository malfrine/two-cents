import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

import firebase_admin.auth as firebase_auth
from rest_framework import serializers, status
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.users.models import User, WaitlistUser
from core.apps.users.serializers import UserWriteSerializer
from core.config.settings import DEBUG

from core.config.settings import DOMAIN

def send_welcome_email(to_email, referral_id):

    context = {
        "referral_code": referral_id,
        "domain": DOMAIN
    }

    text_content = render_to_string("mail/welcome.txt", context=context)
    msg = EmailMultiAlternatives(
        subject="Welcome to the Two Cents waitlist",
        from_email="Malfy from Two Cents <malfy@two-cents.ca>",
        body=text_content,
        to=(to_email,)
    )
    html_content = render_to_string("mail/welcome.html", context)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def create_user(serializer: UserWriteSerializer):
    
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get("email")
    password = serializer.validated_data.get("password")

    if not DEBUG:
        # check waitlist only in prod
        try:
            waitlist_user = WaitlistUser.objects.get(email__iexact=email)
        except WaitlistUser.DoesNotExist:
            raise serializers.ValidationError("Given email is not in waitlist - please request access",
                                                code=status.HTTP_404_NOT_FOUND)
        if not waitlist_user.can_register:
            raise serializers.ValidationError("Given email is on waitlist but not authorized to register account",
                                                code=status.HTTP_403_FORBIDDEN)
    try:
        firebase_auth.create_user(
            email=email,
            password=password
        )
    except Exception:
        raise serializers.ValidationError("Firebase error", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    user = serializer.save()
    user.save()
    FinancialProfile.objects.create_default(user)
    return user

def delete_user(user: User):
    logging.info(f"Deleteing user {user.email}")
    firebase_user = firebase_auth.get_user_by_email(email=user.email)
    firebase_auth.delete_user(firebase_user.uid)
    user.delete()