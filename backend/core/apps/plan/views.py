from rest_framework import viewsets, status
from rest_framework.response import Response

from core.apps.plan.services import make_pennies_request_and_run


class UserPlanViewSet(viewsets.GenericViewSet):
    def list(self, request, format=None):
        data = make_pennies_request_and_run(
            request.user.financial_data, request.user.email
        )
        if data is None:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=data, status=status.HTTP_200_OK)
