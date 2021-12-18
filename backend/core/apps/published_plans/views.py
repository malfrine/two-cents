from rest_framework import viewsets, status
from rest_framework.response import Response

from core.apps.finances.utilities import copy_financial_data
from core.apps.plan.services import make_pennies_request_and_run
from core.apps.published_plans.models import PublishedPlan


class PublishedPlansViewset(viewsets.ViewSet):
    def retrieve(self, request, pk, format=None):
        try:
            published_plan = PublishedPlan.objects.get(pk=pk)
            return make_pennies_request_and_run(published_plan.financial_data)
        except PublishedPlan.DoesNotExist:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, format=None):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        financial_data = copy_financial_data(request.user.financial_data)
        PublishedPlan.objects.create(financial_data=financial_data)
        return Response(status=status.HTTP_200_OK)
