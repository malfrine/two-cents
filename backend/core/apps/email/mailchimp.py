from datetime import datetime
from enum import Enum
import hashlib
import json
import logging

from mailchimp_marketing.api_client import ApiClientError
from core.apps.finances.models.financial_profile import FinancialProfile
from rest_framework import status

from core.apps.users.models import User
from core.config.settings import mailchimp, TWO_CENTS_AUDIENCE_ID


def get_mailchimp_email_hash(user_email: str):
    return hashlib.md5(user_email.encode("utf-8").lower()).hexdigest()


get_mailchimp_id = get_mailchimp_email_hash


class MailchimpUserTags(Enum):
    NEW_USER = "New User"
    PREMIUM_USER = "Premium User"


class MailchimpErrors(Enum):
    MEMBER_EXISTS = "Member Exists"


def _make_active_tag(user_tag: MailchimpUserTags):
    return {"tags": [{"name": user_tag.value, "status": "active"}]}


def make_new_user_tags():
    return _make_active_tag(MailchimpUserTags.NEW_USER)


def make_premium_user_tags():
    return _make_active_tag(MailchimpUserTags.PREMIUM_USER)


def make_member_info_data(user: User, financial_profile: FinancialProfile):
    birth_date: datetime = financial_profile.birth_date
    birthday_str = f"{birth_date.month}/{birth_date.day}"

    return {
        "email_address": user.email,
        "status": "subscribed",
        "merge_fields": {
            "FNAME": user.first_name,
            "BIRTHDAY": birthday_str,
            # TODO: get user last name
        },
    }


def create_mailchimp_user(user: User, financial_profile: FinancialProfile):

    member_info = make_member_info_data(user, financial_profile)
    tags_data = make_new_user_tags()

    try:
        mailchimp.lists.add_list_member(TWO_CENTS_AUDIENCE_ID, member_info)
        mailchimp_id = get_mailchimp_id(user.email)
        mailchimp.lists.update_list_member_tags(
            TWO_CENTS_AUDIENCE_ID, mailchimp_id, tags_data
        )
    except ApiClientError as error:
        if error.status_code == status.HTTP_400_BAD_REQUEST:
            d = json.loads(error.text)
            if d.get("title") == MailchimpErrors.MEMBER_EXISTS.value:
                return  # nbd if member already exists
        logging.error(
            f"Unable to add {user.email} to mailchimp Two Cents audience becase of {error.text}"
        )


def set_mailchimp_user_as_premium(user: User):
    tags_data = make_premium_user_tags()
    try:
        mailchimp_id = get_mailchimp_id(user.email)
        mailchimp.lists.update_list_member_tags(
            TWO_CENTS_AUDIENCE_ID, mailchimp_id, tags_data
        )
    except ApiClientError as error:
        logging.error(
            f"Unable to updated {user.email} as Premium User in mailchimp because of {error.text}"
        )


def delete_mailchimp_user(user: User):
    try:
        mailchimp_id = get_mailchimp_id(user.email)
        mailchimp.lists.delete_list_member(TWO_CENTS_AUDIENCE_ID, mailchimp_id)
    except ApiClientError as error:
        if error.status_code == status.HTTP_404_NOT_FOUND:
            return  # member not found - nbd
        logging.error(
            f"Unable to delete {user.email} from mailchimp because of {error.text}"
        )
