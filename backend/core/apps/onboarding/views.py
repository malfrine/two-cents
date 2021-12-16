import logging
from datetime import datetime

from dateutil.parser import parse
from rest_framework import views, serializers, status
from rest_framework.response import Response
from core.apps.email.mailchimp import create_mailchimp_user

from core.apps.finances.models.constants import InterestTypes
from core.apps.finances.models.financial_profile import FinancialProfile
from core.apps.finances.models.goals import FinancialGoal, GoalType
from core.apps.finances.models.investments import (
    Investment,
    InvestmentType,
    RiskChoices,
    get_risk_level_map,
    InvestmentAccountType,
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

NEST_EGG_MONTHS = 6


def create_financial_profile(user, data):
    try:
        financial_profile = FinancialProfile.objects.get(
            financial_data=user.financial_data
        )
    except FinancialProfile.DoesNotExist:
        financial_profile = FinancialProfile.objects.create_default()
    fp_serializer = FinancialProfileSerializer(financial_profile, data=data)
    fp_serializer.is_valid(raise_exception=True)
    financial_profile = fp_serializer.save(financial_data=user.financial_data)
    return financial_profile


def create_goals(user, data):
    big_purchase = data.get("big_purchase")
    if big_purchase is not None:
        big_purchase_goal = FinancialGoal(
            financial_data=user.financial_data,
            name="Big Purchase",
            type=GoalType.BIG_PURCHASE,
            amount=big_purchase.get("amount"),
            date=big_purchase.get("date"),
        )
        big_purchase_goal.save()
    nest_egg = data.get("current_nest_egg_amount")
    if nest_egg is not None:
        cash_account = Investment(
            financial_data=user.financial_data,
            name="Cash Account",
            current_balance=nest_egg,
            investment_type=InvestmentType.CASH,
            account_type=InvestmentAccountType.NON_REGISTERED.value,
        )
        cash_account.save()
        financial_profile, _ = FinancialProfile.objects.get_or_create(
            financial_data=user.financial_data
        )
        nest_egg_target = financial_profile.monthly_expenses_estimate * NEST_EGG_MONTHS
        nest_egg_goal = FinancialGoal(
            financial_data=user.financial_data,
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
    logging.warning(
        f"Couldn't find default risk choise for risk tolerance: {risk_tolerance}"
    )
    return RiskChoices.MEDIUM


def create_investments(user, data):
    financial_profile, _ = FinancialProfile.objects.get_or_create(
        financial_data=user.financial_data
    )
    risk_level = get_default_investment_risk_level(financial_profile.risk_tolerance)
    tfsa = Investment(
        financial_data=user.financial_data,
        name="TFSA Portfolio",
        current_balance=data.get("tfsa", 0),
        investment_type=InvestmentType.PORTFOLIO,
        account_type=InvestmentAccountType.TFSA.value,
        risk_level=risk_level,
    )
    tfsa.save()
    rrsp = Investment(
        financial_data=user.financial_data,
        name="RRSP Portfolio",
        current_balance=data.get("rrsp", 0),
        investment_type=InvestmentType.PORTFOLIO,
        account_type=InvestmentAccountType.RRSP.value,
        risk_level=risk_level,
    )
    rrsp.save()
    non_registered = Investment(
        financial_data=user.financial_data,
        name="Non Registerd Portfolio",
        current_balance=data.get("non_registered", 0),
        account_type=InvestmentAccountType.NON_REGISTERED.value,
        risk_level=risk_level,
    )
    non_registered.save()


def create_loans(user, data):
    for loan_type, loan_info in data.items():
        loan_type_enum: LoanType = LoanType(loan_type)
        apr = get_default_apr(loan_type_enum)
        balance = abs(float(loan_info.get("balance", 0)))
        data = {
            "name": loan_type,
            "financial_data": user.financial_data.pk,
            "current_balance": balance,
            "loan_interest": {"interest_type": InterestTypes.FIXED.value, "apr": apr},
            "loan_type": loan_type_enum.value,
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
        serializer.save(financial_data=user.financial_data)


class OnboardingAPIView(views.APIView):

    MANDATORY_DATA_FIELDS = {
        "account",
        "financial_profile",
        "goals",
        "investments",
        "loans",
    }

    def post(self, request, format=None):
        data_keys = set(request.data.keys())
        if not self.MANDATORY_DATA_FIELDS.issubset(data_keys):
            logging.error(
                "Unable to onboard user because of bad request", extra=request.data
            )
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=f"Missing one of the following mandatory fields: {self.MANDATORY_DATA_FIELDS}",
            )
        user = None
        try:
            user = create_user(
                UserWriteSerializer(data=request.data.get("account", dict()))
            )
            if user is None:
                return Response(data=None, status=status.HTTP_400_BAD_REQUEST)
            financial_profile = create_financial_profile(
                user, request.data.get("financial_profile", dict())
            )
            create_mailchimp_user(user, financial_profile)
            create_goals(user, request.data.get("goals", dict()))
            create_investments(user, request.data.get("investments", dict()))
            create_loans(user, request.data.get("loans", dict()))
        except serializers.ValidationError as e:
            if user is not None:
                delete_user(user)
            data = None
            if status.is_client_error(e.status_code):
                data = e.detail
            logging.error(
                f"Unable to onboard user because of {e.status_code} status",
                extra={"data": request.data, "error": data},
            )
            return Response(status=e.status_code, data=data)
        return Response(status=status.HTTP_200_OK)
