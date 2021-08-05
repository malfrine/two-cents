from django.test import TestCase

from core.apps.users.serializers import UserWriteSerializer
from core.apps.users.utilities import create_user, delete_user


class UserTestCase(TestCase):
    def test_user_create_and_delete(self):
        """Create user and delete user"""
        data = {"email": "django_test@user.ca", "password": "test_user_password"}

        user = create_user(UserWriteSerializer(data=data))

        delete_user(user)
