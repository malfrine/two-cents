from rest_framework import status
from rest_framework.response import Response

from core.apps.finances.models.loans import LoanType, INSTALMENT_LOANS, REVOLVING_LOANS
from core.apps.finances.models.constants import InterestTypes
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.investments import (
    Investment,
    INVESTMENT_REQUIRED_FIELDS_MAP,
    RiskChoices,
    VolatilityChoices,
)
from core.apps.finances.models.financial_profile import Loan
from rest_framework import viewsets

from core.apps.finances.serializers import (
    FinancialProfileSerializer,
    InvestmentSerializer,
    LoanSerializer,
    UserFinancesSerializer,
)


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
        return Response(self.get_serializer(request.user).data)


class FinancesEnumsViewset(viewsets.GenericViewSet):
    def list(self, request):

        d = dict()
        for name in REVOLVING_LOANS:
            d[name.value] = "revolving"
        for name in INSTALMENT_LOANS:
            d[name.value] = "instalment"

        data = {
            "loan_types": d,
            "interest_types": list(name for name in InterestTypes),
            "investment_fields": INVESTMENT_REQUIRED_FIELDS_MAP,
            "risk_levels": list(name for name in RiskChoices),
            "volatility_choices": list(name for name in VolatilityChoices),
        }
        return Response(data)
