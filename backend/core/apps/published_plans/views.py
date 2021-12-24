from rest_framework import viewsets, status
from rest_framework.response import Response

from core.apps.finances.utilities import copy_financial_data
from core.apps.plan.services import make_pennies_request_and_run
from core.apps.published_plans.models import PublishedPlan
from core.apps.published_plans.serializers import PublishedPlanSerializer


class PublishedPlansViewset(viewsets.GenericViewSet):

    serializer_class = PublishedPlanSerializer

    def get_object(self):
        pk = self.kwargs.get("pk")
        if pk is None:
            raise KeyError("pk must be in kwargs")
        return PublishedPlan.objects.get(pk=pk)

    def retrieve(self, request, pk, format=None):
        try:
            published_plan = self.get_object()
            serializer = self.get_serializer(published_plan)
            pennies_data = make_pennies_request_and_run(published_plan.financial_data)
            if pennies_data is None:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # NB: could maybe have written a method in the `PublishedPlanSerializer` to run pennies but i wanted it
            # to be more explicit
            data = dict(serializer.data)
            data["plans"] = pennies_data
            return Response(data=data)
        except PublishedPlan.DoesNotExist:
            print(self.kwargs)
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, format=None):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN)
        financial_data = copy_financial_data(request.user.financial_data)
        published_plan = PublishedPlan.objects.create(financial_data=financial_data)
        return Response(status=status.HTTP_200_OK, data={"id": published_plan.id})
