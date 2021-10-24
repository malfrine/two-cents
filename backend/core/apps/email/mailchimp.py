from datetime import datetime
import hashlib
import logging

from mailchimp_marketing.api_client import ApiClientError
from core.apps.finances.models.financial_profile import FinancialProfile

from core.apps.users.models import User
from core.config.settings import mailchimp, TWO_CENTS_AUDIENCE_ID


def get_mailchimp_email_hash(user_email: str):
    return hashlib.md5(user_email.encode("utf-8").lower()).hexdigest()


get_mailchimp_id = get_mailchimp_email_hash


def create_mailchimp_user(user: User, financial_profile: FinancialProfile):

    birth_date: datetime = financial_profile.birth_date
    birthday_str = f"{birth_date.month}/{birth_date.day}"

    member_info = {
        "email_address": user.email,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": user.first_name,
            "BIRTHDAY": birthday_str,
            # TODO: get user last name
        },
    }

    tags_data = {"tags": [{"name": "New User", "status": "active"}]}

    try:
        mailchimp.lists.add_list_member(TWO_CENTS_AUDIENCE_ID, member_info)
        mailchimp_id = get_mailchimp_id(user.email)
        mailchimp.lists.update_list_member_tags(
            TWO_CENTS_AUDIENCE_ID, mailchimp_id, tags_data
        )
    except ApiClientError as error:
        logging.error(
            f"Unable to add {user.email} to mailchimp Two Cents audience becase of {error}"
        )
