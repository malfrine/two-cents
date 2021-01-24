import re
from django.db.models.query import QuerySet
import requests
from uuid import uuid4

from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.sessions.models import Session
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from rest_framework import mixins, views, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers

from core.apps.users.models import User
from core.apps.users.serializers import UserWriteSerializer


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
        if self.request.data.get("password") is None:
            raise serializers.ValidationError("Password is required.")
        user = serializer.save()
        user.set_password(self.request.data.get("password"))
        user.save()
