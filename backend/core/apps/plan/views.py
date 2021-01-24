from django.shortcuts import render

from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response
from core.apps.finances.serializers import PenniesRequestSerializer
from core.apps.pennies.pennies.solver import solve_request

# Create your views here.
from pennies.model.status import PenniesStatus


class UserPlanViewSet(viewsets.GenericViewSet):
    def list(self, request, format=None):
        pennies_request = PenniesRequestSerializer(request.user)
        pennies_response = solve_request(pennies_request.data)
        print(pennies_response)
        if pennies_response["status"] == PenniesStatus.SUCCESS:
            return Response(status=status.HTTP_200_OK, data=pennies_response["result"])
        else:
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data=pennies_response["result"],
            )
