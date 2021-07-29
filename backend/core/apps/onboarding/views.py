import logging
from datetime import datetime

from dateutil.parser import parse
from rest_framework import views, serializers, status
from rest_framework.response import Response

from core.apps.finances.models.constants import InterestTypes
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.goals import FinancialGoal, GoalType
from core.apps.finances.models.investments import (
    Investment,
    InvestmentType,
    RiskChoices,
    get_risk_level_map,
)
from core.apps.finances.models.loans import (
    Loan,
    LoanType,
    get_default_apr,
)
from core.apps.finances.serializers.serializers import FinancialProfileSerializer
from core.apps.finances.serializers.views.loan import LoanSerializer
from core.apps.finances.utilities import (
    calculate_instalment_loan_min_payment,
    calculate_revolving_loan_min_payment,
)
from core.apps.users.serializers import UserWriteSerializer
from core.apps.users.utilities import create_user, delete_user
from pennies.model.constants import InvestmentAccountType

NEST_EGG_MONTHS = 6


def create_financial_profile(user, data):
    financial_profile = FinancialProfile.objects.get(user=user)
    fp_serializer = FinancialProfileSerializer(financial_profile, data=data)
    fp_serializer.is_valid(raise_exception=True)
    financial_profile = fp_serializer.save(user=user)
    return financial_profile


def create_goals(user, data):
    big_purchase = data.get("big_purchase")
    if big_purchase is not None:
        big_purchase_goal = FinancialGoal(
            user=user,
            name="Big Purchase",
            type=GoalType.BIG_PURCHASE,
            amount=big_purchase.get("amount"),
            date=big_purchase.get("date"),
        )
        big_purchase_goal.save()
    nest_egg = data.get("current_nest_egg_amount")
    if nest_egg is not None:
        cash_account = Investment(
            user=user,
            name="Cash Account",
            current_balance=nest_egg,
            investment_type=InvestmentType.CASH,
            account_type=InvestmentAccountType.NON_REGISTERED.value,
        )
        cash_account.save()
        financial_profile, _ = FinancialProfile.objects.get_or_create(user=user)
        nest_egg_target = financial_profile.monthly_expenses_estimate * NEST_EGG_MONTHS
        nest_egg_goal = FinancialGoal(
            user=user,
            name="Nest Egg",
            type=GoalType.NEST_EGG,
            amount=nest_egg_target,
            date=datetime.now().date(),
        )
        nest_egg_goal.save()


def get_default_investment_risk_level(risk_tolerance: float):
    risk_level_map = get_risk_level_map()
    risk_tolerance = int(risk_tolerance)
    for (lower_bound, upper_bound), risk_choice in risk_level_map.items():
        if lower_bound <= risk_tolerance <= upper_bound:
            return risk_choice
    logging.warn(
        f"Couldn't find default risk choise for risk tolerance: {risk_tolerance}"
    )
    return RiskChoices.MEDIUM


def create_investments(user, data):
    financial_profile, _ = FinancialProfile.objects.get_or_create(user=user)
    risk_level = get_default_investment_risk_level(financial_profile.risk_tolerance)
    tfsa = Investment(
        user=user,
        name="TFSA Portfolio",
        current_balance=data.get("tfsa", 0),
        investment_type=InvestmentType.PORTFOLIO,
        account_type=InvestmentAccountType.TFSA.value,
        risk_level=risk_level,
    )
    tfsa.save()
    rrsp = Investment(
        user=user,
        name="RRSP Portfolio",
        current_balance=data.get("rrsp", 0),
        investment_type=InvestmentType.PORTFOLIO,
        account_type=InvestmentAccountType.RRSP.value,
        risk_level=RiskChoices.LOW,
    )
    rrsp.save()
    non_registered = Investment(
        user=user,
        name="Non Registerd Portfolio",
        current_balance=data.get("non_registered", 0),
        account_type=InvestmentAccountType.NON_REGISTERED.value,
        risk_level=risk_level,
    )
    non_registered.save()


def create_loans(user, data):
    for loan_type, loan_info in data.items():
        loan_type_enum = LoanType(loan_type)
        apr = get_default_apr(loan_type_enum)
        balance = abs(float(loan_info.get("balance", 0)))
        data = {
            "name": loan_type,
            "user": user,
            "current_balance": balance,
            "loan_interest": {"interest_type": InterestTypes.FIXED.value, "apr": apr},
            "loan_type": loan_type_enum,
        }

        if Loan.is_instalment_loan(loan_type=loan_type_enum):
            end_date_str = loan_info.get("date")
            if end_date_str is None:
                serializers.ValidationError("Instalment loans must have an end date")
            end_date = parse(end_date_str).date()
            minimum_monthly_payment = calculate_instalment_loan_min_payment(
                balance, apr, end_date
            )
            data["end_date"] = end_date
            data["minimum_monthly_payment"] = minimum_monthly_payment
        elif loan_type_enum == LoanType.MORTGAGE:
            end_date_str = loan_info.get("date")
            if end_date_str is None:
                serializers.ValidationError("Mortgage loans must have an end date")
            end_date = parse(end_date_str).date()
            current_term_end_date = end_date
            minimum_monthly_payment = calculate_instalment_loan_min_payment(
                balance, apr, end_date
            )
            data["end_date"] = end_date
            data["minimum_monthly_payment"] = minimum_monthly_payment
            data["current_term_end_date"] = current_term_end_date
        else:
            data["minimum_monthly_payment"] = calculate_revolving_loan_min_payment(
                balance, apr
            )

        serializer = LoanSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)


class OnboardingAPIView(views.APIView):

    MANDATORY_DATA_FIELDS = set(
        ("account", "financial_profile", "goals", "investments", "loans")
    )

    def post(self, request, format=None):
        data_keys = set(request.data.keys())
        if not self.MANDATORY_DATA_FIELDS.issubset(data_keys):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=f"Missing one of the following mandatory fields: {self.MANDATORY_DATA_FIELDS}",
            )
        user = None
        try:
            user = create_user(UserWriteSerializer(data=request.data.get("account")))
            create_financial_profile(user, request.data.get("financial_profile"))
            create_goals(user, request.data.get("goals"))
            create_investments(user, request.data.get("investments"))
            create_loans(user, request.data.get("loans"))
        except serializers.ValidationError as e:
            if user is not None:
                delete_user(user)
            data = None
            if status.is_client_error(e.status_code):
                data = e.detail
            return Response(status=e.status_code, data=data)
        return Response(status=status.HTTP_200_OK)
