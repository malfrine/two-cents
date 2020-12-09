from django.contrib.auth import get_user
from django.core.serializers import get_serializer
from rest_framework import generics, mixins, permissions, request, status
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import views
from rest_framework.response import Response
from core.apps.finances import serializers
from core.apps.finances.models import FinancialProfile, Investment, Loan
from rest_framework import viewsets

from core.apps.finances.serializers import FinancialProfileSerializer, InvestmentSerializer, LoanSerializer, UserFinancesSerializer
from core.apps.users.models import User



# Create your views here.
class LoanViewset(viewsets.ModelViewSet):
    queryset = Loan.objects.none()
    serializer_class = LoanSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Loan.objects.none()
        else:
            return self.request.user.loans.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class InvestmentViewset(viewsets.ModelViewSet):
    queryset = Investment.objects.none()
    serializer_class = InvestmentSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Investment.objects.none()
        else:
            return self.request.user.investments.all()

    def perform_create(self, serializer):
        # TODO: check if anonymous users can actually add investments
        return serializer.save(user=self.request.user)

class FinancialProfileView(viewsets.GenericViewSet):
    serializer_class = FinancialProfileSerializer

    def get_object(self):
        try:
            return FinancialProfile.objects.get(user=self.request.user)
        except FinancialProfile.DoesNotExist:
            return None

    def list(self, request, format=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        instance =  self.get_object()
        if instance: # update instead of create
            serializer = self.get_serializer(instance, data=request.data)
            success_status = status.HTTP_200_OK
        else: # create
            serializer = self.get_serializer(data=request.data)
            success_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=success_status)

class UserFinancesViewset(viewsets.GenericViewSet):
    serializer_class = UserFinancesSerializer

    def list(self, request):
        return Response(self.get_serializer(request.user).data)
