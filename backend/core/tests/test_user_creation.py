from django.test import TestCase

from core.apps.users.serializers import UserWriteSerializer
from core.apps.users.utilities import create_user, delete_user
from core.tests._utilities import delete_user_if_exists, delete_firebase_user_if_exists


class UserTestCase(TestCase):
    def test_user_create_and_delete(self):
        """Create user and delete user"""
        email = "django_test@user.ca"
        delete_user_if_exists(email)
        delete_firebase_user_if_exists(email)
        data = {
            "email": email,
            "password": "test_user_password",
            "first_name": "Test First Name",
        }
        user = create_user(UserWriteSerializer(data=data))

        delete_user(user)
