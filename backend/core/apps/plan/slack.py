import json

import requests

from core.config.settings import SLACK_WEBHOOK_URL


def _make_data(data):
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Pennies failed on this request:",
                },
            },
            {
                "type": "context",
                "elements": [
                    {"type": "plain_text", "text": json.dumps(data, indent=4)}
                ],
            },
        ]
    }


def send_failed_request_data_to_slack(pennies_request):
    response = requests.post(
        SLACK_WEBHOOK_URL,
        data=json.dumps(_make_data(pennies_request.data), indent=4),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 200:
        raise ValueError(
            "Request to slack returned an error %s, the response is:\n%s"
            % (response.status_code, response.text)
        )


def send_failed_request_message():
    error_block = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Pennies failed, check sentry for details",
                },
            }
        ]
    }
    response = requests.post(
        SLACK_WEBHOOK_URL,
        data=json.dumps(error_block, indent=4),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code != 200:
        raise ValueError(
            "Request to slack returned an error %s, the response is:\n%s"
            % (response.status_code, response.text)
        )
