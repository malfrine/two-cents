import re

from django.contrib.auth.base_user import BaseUserManager
from django.db.models.query import QuerySet
import requests
from uuid import uuid4

from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.sessions.models import Session
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from rest_framework import mixins, views, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers

from core.apps.users.models import User, WaitlistUser
from core.apps.users.serializers import UserWriteSerializer, WaitlistUserSerializer


class SessionAPIView(views.APIView):
    def get(self, request, format=None):
        """Return session cookie in header if session exists"""
        user = get_user(request)
        print(user)
        if not user.is_anonymous and user.is_authenticated:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        """Crete a new session by logging in"""
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, format=None):
        """Destroy a session and throw out the cookie"""
        try:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserWriteSerializer
    queryset = User.objects.none()

    def perform_create(self, serializer):
        try:
            waitlist_user = WaitlistUser.objects.get(email=self.request.data.get("email"))
        except WaitlistUser.DoesNotExist:
            raise serializers.ValidationError("Given email is not in waitlist - please request access", code=status.HTTP_404_NOT_FOUND)
        if not waitlist_user.can_register:
            raise serializers.ValidationError("Given email is on waitlist but not authorized to register account", code=status.HTTP_403_FORBIDDEN)
        if self.request.data.get("password") is None:
            raise serializers.ValidationError("Password is required.")
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()


class WaitlistUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = WaitlistUserSerializer

    def perform_create(self, serializer):
        waitlist_user = serializer.save()
        waitlist_user.email = BaseUserManager.normalize_email(waitlist_user.email)
        waitlist_user.referral_id = waitlist_user.id
        
        text_content = render_to_string("mail/welcome.txt")
        msg = EmailMultiAlternatives(
            subject="Welcome to the Two Cents waitlist",
            from_email="Malfy from Two Cents <malfy@two-cents.ca>",
            body=text_content,
            to=(waitlist_user.email,)
        )
        html_content = render_to_string("mail/welcome.html")
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        waitlist_user.save()

