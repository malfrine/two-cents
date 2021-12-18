from rest_framework import viewsets

from core.apps.plan.services import make_pennies_request_and_run


class UserPlanViewSet(viewsets.GenericViewSet):
    def list(self, request, format=None):
        return make_pennies_request_and_run(
            request.user.financial_data, request.user.email
        )
