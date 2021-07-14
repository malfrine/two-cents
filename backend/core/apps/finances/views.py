from django.contrib.auth.models import AnonymousUser
from firebase_admin.auth import UserRecord as FirebaseUserRecord
from rest_framework import status
from rest_framework.response import Response

from core.apps.finances.models.goals import FinancialGoal
from core.apps.finances.models.loans import LOAN_REQUIRED_FIELDS_MAP, LOAN_INTEREST_REQUIRED_FIELDS_MAP
from core.apps.finances.models.constants import InterestTypes
from core.apps.finances.models.financial_profile import FinancialProfile, Province
from core.apps.finances.models.investments import (
    Investment,
    INVESTMENT_REQUIRED_FIELDS_MAP,
    RiskChoices,
    VolatilityChoices, InvestmentAccountType,
)
from core.apps.finances.models.financial_profile import Loan
from rest_framework import viewsets

from core.apps.finances.serializers.serializers import (
    FinancialProfileSerializer,
    InvestmentSerializer,
    UserFinancesSerializer, FinancialGoalSerializer,
)
from core.apps.finances.serializers.pennies.request import PenniesRequestSerializer
from core.apps.finances.serializers.views.loan import LoanSerializer


# Create your views here.
from core.apps.users.models import User


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


class FinancialGoalViewset(viewsets.ModelViewSet):
    queryset = FinancialGoal.objects.none()
    serializer_class = FinancialGoalSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return FinancialGoal.objects.none()
        else:
            return self.request.user.goals.all()

    def perform_create(self, serializer):
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
        instance = self.get_object()
        if instance:  # update instead of create
            serializer = self.get_serializer(instance, data=request.data)
            success_status = status.HTTP_200_OK
        else:  # create
            serializer = self.get_serializer(data=request.data)
            success_status = status.HTTP_201_CREATED
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=success_status)


class UserFinancesViewset(viewsets.GenericViewSet):
    serializer_class = UserFinancesSerializer

    def list(self, request):
        if isinstance(request.user, User):
            return Response(self.get_serializer(request.user).data)
        elif isinstance(request.user, FirebaseUserRecord):
            user = User.objects.create_user(email=request.user.email)
            FinancialProfile.objects.create_default(user)
            return Response(self.get_serializer(user).data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PenniesRequestViewset(viewsets.GenericViewSet):
    serializer_class = PenniesRequestSerializer

    def list(self, request):
        return Response(self.get_serializer(request.user).data)


class FinancesEnumsViewset(viewsets.GenericViewSet):
    def list(self, request):

        data = {
            "interest_types": list(name for name in InterestTypes),
            "investment_fields": INVESTMENT_REQUIRED_FIELDS_MAP,
            "loan_fields": LOAN_REQUIRED_FIELDS_MAP,
            "loan_interest_types_fields": LOAN_INTEREST_REQUIRED_FIELDS_MAP,
            "risk_levels": list(name for name in RiskChoices),
            "volatility_choices": list(name for name in VolatilityChoices),
            "provinces": list(name for name in Province),
            "investment_account_types": list(name for name in InvestmentAccountType)
        }
        return Response(data)
