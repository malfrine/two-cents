from datetime import date
from django.test import TestCase

from core.apps.finances.utilities import get_first_date_of_next_month


class UtilitiesTestCase(TestCase):
    def test_first_date_of_next_month(self):
        """Create user and delete user"""
        assert date(2021, 12, 1) == get_first_date_of_next_month(date(2021, 11, 1))
        assert date(2022, 1, 1) == get_first_date_of_next_month(date(2021, 12, 1))
        assert date(2022, 1, 1) == get_first_date_of_next_month(date(2021, 12, 10))
