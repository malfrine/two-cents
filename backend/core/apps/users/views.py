import logging

from django.contrib.auth import authenticate, get_user, login, logout
from rest_framework import mixins, views, viewsets, status
from rest_framework.response import Response

from core.apps.users.models import User, WaitlistUser, create_waitlist_user
from core.apps.users.serializers import UserWriteSerializer
from core.apps.users.utilities import create_user, send_welcome_email


class SessionAPIView(views.APIView):
    def get(self, request, format=None):
        """Return session cookie in header if session exists"""
        user = get_user(request)
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
        except:  # noqa
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AccountViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = UserWriteSerializer
    queryset = User.objects.none()

    def perform_create(self, serializer):
        return create_user(serializer)


class WaitlistUserAPIView(views.APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        if email is None:
            return Response(
                data={"message": "Email and first name required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        referree_id = request.data.get("referree_id")
        try:
            waitlist_user = WaitlistUser.objects.get(email__iexact=email)
        except WaitlistUser.DoesNotExist:
            logging.info(f"User with {email} does not exist - making new object")
            waitlist_user = create_waitlist_user(email, referree_id)
            send_welcome_email(waitlist_user.email, waitlist_user.referral_id)
        return Response(
            data={
                "email": waitlist_user.email,
                "referral_id": str(waitlist_user.referral_id),
            }
        )
