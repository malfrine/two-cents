from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from core.apps.finances.serializers import PenniesRequestSerializer
from core.apps.pennies.pennies.solver import process_request

# Create your views here.
class UserPlanViewSet(viewsets.GenericViewSet):
    def list(self, request, format=None):
        pennies_request = PenniesRequestSerializer(request.user)

        # TODO: make cache to store existing solutions
        return Response(process_request(pennies_request.data))
