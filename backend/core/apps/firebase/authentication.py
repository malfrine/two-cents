import os
from dataclasses import dataclass
from pathlib import Path

import firebase_admin
from django.contrib.auth.models import AnonymousUser
from firebase_admin import auth, credentials
from firebase_admin.auth import InvalidIdTokenError
from rest_framework import authentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from core.apps.users.models import User
from pennies.model.financial_profile import FinancialProfile

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": os.environ.get('FIREBASE_SA_PROJECT_ID'),
  "private_key_id": os.environ.get('FIREBASE_SA_PRIVATE_KEY_ID'),
  "private_key": os.environ.get('FIREBASE_SA_PRIVATE_KEY').replace('\\n', '\n'),
  "client_email": os.environ.get('FIREBASE_SA_CLIENT_EMAIL'),
  "client_id": os.environ.get('FIREBASE_SA_CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://accounts.google.com/o/oauth2/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CERT_URL')
})
default_app = firebase_admin.initialize_app(cred)

class FirebaseAuthentication(authentication.TokenAuthentication):
    def authenticate(self, request):
        header = get_authorization_header(request)

        try:
            id_token = header.decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        if not id_token:
            return (AnonymousUser, None)

        try:
            decoded_token = auth.verify_id_token(id_token)
        except InvalidIdTokenError:
            return (AnonymousUser, None)
        uid = decoded_token.get("uid")
        firebase_user = auth.get_user(uid)

        try:
            user = User.objects.get(email__iexact=firebase_user.email)
            print(f"Firebase recognized the user to be a registered user {(user.pk, user.email)}")
        except User.DoesNotExist:
            user = firebase_user
            print(f"Firebase recognized the user to be a non-registered user {(user.email)}")

        return (user, None)
