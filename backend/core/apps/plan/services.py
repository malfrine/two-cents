import json
import logging

from rest_framework import status
from rest_framework.response import Response

from core.apps.finances.models.financial_data import FinancialData
from core.apps.finances.serializers.pennies.request import PenniesRequestSerializer
from core.apps.pennies.pennies.main import solve_request

# Create your views here.
from core.apps.plan.slack import send_failed_request_message
from core.config.settings import DEBUG
from pennies.model.status import PenniesStatus


def make_pennies_request_and_run(
    financial_data: FinancialData, email: str = "unknown"
) -> Response:
    pennies_request = PenniesRequestSerializer(financial_data)
    logging.info(
        f"Info About to build a plan for {email}",
        exc_info=True,
        extra={"request": pennies_request.data},
    )
    pennies_response = solve_request(pennies_request.data)
    if pennies_response["status"] == PenniesStatus.SUCCESS:
        return Response(status=status.HTTP_200_OK, data=pennies_response["result"])
    else:
        if not DEBUG:
            logging.error(
                "Failed to generate a plan with the following request",
                exc_info=True,
                extra={
                    # Optionally pass a request and we'll grab any information we can
                    "request": pennies_request.data,
                },
            )
            send_failed_request_message()
        else:
            print(json.dumps(pennies_request.data, indent=3))
            print(pennies_response["result"])
        return Response(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            data=pennies_response["result"],
        )
