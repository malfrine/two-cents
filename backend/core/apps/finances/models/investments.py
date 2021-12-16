from datetime import date
from typing import Dict, Tuple

from django.db import models

from core.apps.finances.models.constants import InterestTypes
from core.apps.finances.models.financial_data import FinancialData
from core.utilities import get_months_between


class InvestmentType(models.TextChoices):
    MUTUAL_FUND = "Mutual Fund", "Mutual Fund"
    ETF = "ETF", "Exchange Traded Fund"
    GIC = "GIC", "Guaranteed Investment Certificate"
    TERM_DEPOSIT = "Term Deposit", "Term Deposit"
    STOCK = "Stock", "Stock"
    BOND = "Bond", "Bond"  # TODO
    CASH = "Cash", "Cash"
    PORTFOLIO = "Portfolio", "Portfolio"


class InvestmentAccountType(models.TextChoices):
    NON_REGISTERED = "Non-Registered", "Non-Registered"
    RRSP = "RRSP", "Registered Retirement Savings Plan"
    TFSA = "TFSA", "Tax-Free Savings Account"


def get_required_fields_map():
    all_non_guaranteed_inv_fields = [
        "name",
        "current_balance",
        "investment_type",
        "account_type",
    ]
    all_guaranteed_inv_fields = [
        "name",
        "investment_type",
        "principal_investment_amount",
        "investment_date",
        "maturity_date",
        "interest_type",
        "expected_roi",
        "prime_modifier",
        "account_type",
    ]
    return {
        InvestmentType.MUTUAL_FUND: all_non_guaranteed_inv_fields
        + ["pre_authorized_monthly_contribution", "risk_level"],
        InvestmentType.ETF: all_non_guaranteed_inv_fields
        + ["pre_authorized_monthly_contribution", "risk_level"],
        InvestmentType.GIC: all_guaranteed_inv_fields,
        InvestmentType.TERM_DEPOSIT: all_guaranteed_inv_fields,
        InvestmentType.STOCK: all_non_guaranteed_inv_fields
        + [
            "pre_authorized_monthly_contribution",
            "symbol",
            "expected_roi",
            "volatility_choice",
        ],
        InvestmentType.CASH: all_non_guaranteed_inv_fields
        + ["pre_authorized_monthly_contribution"],
        InvestmentType.PORTFOLIO: all_non_guaranteed_inv_fields
        + ["pre_authorized_monthly_contribution", "risk_level"],
    }


INVESTMENT_REQUIRED_FIELDS_MAP = get_required_fields_map()


class RiskChoices(models.TextChoices):
    LOW = "Low", "Low Risk"
    MEDIUM = "Medium", "Medium Risk"
    HIGH = "High", "High Risk"


def get_risk_level_map() -> Dict[Tuple[int, int], RiskChoices]:
    return {
        (0, 33): RiskChoices.LOW,
        (34, 67): RiskChoices.MEDIUM,
        (68, 100): RiskChoices.HIGH,
    }


class VolatilityChoices(models.TextChoices):
    VERY_LOW = "Very Low", "Very Low Volatility"
    LOW = "Low", "Low Volatility"
    MEDIUM = "Medium", "Medium Volatility"
    HIGH = "High", "High Volatility"
    VERY_HIGH = "Very High", "Very High Volatility"


class Investment(models.Model):

    _RISK_TO_ROI = {
        RiskChoices.LOW: 3.5,
        RiskChoices.MEDIUM: 5.0,
        RiskChoices.HIGH: 7.0,
    }

    _RISK_TO_VOLATILITY = {
        RiskChoices.LOW: VolatilityChoices.LOW,
        RiskChoices.MEDIUM: VolatilityChoices.MEDIUM,
        RiskChoices.HIGH: VolatilityChoices.HIGH,
    }

    _VOLATILITY_AS_FLOAT = {
        VolatilityChoices.VERY_LOW: 0.5,
        VolatilityChoices.LOW: 2.5,
        VolatilityChoices.MEDIUM: 5,
        VolatilityChoices.HIGH: 7.5,
        VolatilityChoices.VERY_HIGH: 10,
    }

    # attributes for all investments
    @property
    def roi(self) -> float:
        if self.investment_type in [
            InvestmentType.MUTUAL_FUND,
            InvestmentType.ETF,
            InvestmentType.PORTFOLIO,
        ]:
            return self._RISK_TO_ROI[self.risk_level]
        elif self.investment_type in [
            InvestmentType.TERM_DEPOSIT,
            InvestmentType.GIC,
            InvestmentType.STOCK,
        ]:
            return self.expected_roi
        elif self.investment_type in [InvestmentType.CASH]:
            return 0
        else:
            raise ValueError("Given investment type has unknown volatility")

    @property
    def volatility(self) -> float:
        if self.investment_type in [
            InvestmentType.MUTUAL_FUND,
            InvestmentType.ETF,
            InvestmentType.PORTFOLIO,
        ]:
            return self._VOLATILITY_AS_FLOAT[self._RISK_TO_VOLATILITY[self.risk_level]]
        elif self.investment_type in [
            InvestmentType.TERM_DEPOSIT,
            InvestmentType.GIC,
            InvestmentType.CASH,
        ]:
            return 0
        elif self.investment_type == InvestmentType.STOCK:
            return self._VOLATILITY_AS_FLOAT[self.volatility_choice]
        else:
            raise ValueError("Given investment type has unknown volatility")

    financial_data = models.ForeignKey(
        FinancialData, on_delete=models.CASCADE, related_name="investments"
    )
    name = models.CharField(max_length=50)
    current_balance = models.FloatField(
        default=0, blank=True, null=True, verbose_name="Current Balance"
    )
    investment_type = models.CharField(
        max_length=50,
        default=InvestmentType.MUTUAL_FUND,
        choices=InvestmentType.choices,
        verbose_name="Investment Type",
    )
    account_type = models.CharField(
        max_length=50,
        default=InvestmentAccountType.NON_REGISTERED,
        choices=InvestmentAccountType.choices,
        verbose_name="Investment Account Type",
    )
    pre_authorized_monthly_contribution = models.FloatField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Pre-Authorized Monthly Contribution",
    )

    # mutual funds and etfs
    risk_level = models.CharField(
        default=None,
        blank=True,
        null=True,
        max_length=50,
        choices=RiskChoices.choices,
        verbose_name="Risk Type",
    )
    # TODO: contribution end date

    # GICs and term deposits
    principal_investment_amount = models.FloatField(
        default=None, blank=True, null=True, verbose_name="Amount Invested"
    )
    investment_date = models.DateField(
        default=None, blank=True, null=True, verbose_name="Investment Date",
    )
    maturity_date = models.DateField(
        default=None, blank=True, null=True, verbose_name="Maturity Date",
    )

    @property
    def final_month(self):
        if self.investment_type in [InvestmentType.GIC, InvestmentType.TERM_DEPOSIT]:
            return get_months_between(date.today(), self.maturity_date)
        return None

    @property
    def start_month(self):
        if self.investment_type in [InvestmentType.GIC, InvestmentType.TERM_DEPOSIT]:
            return get_months_between(date.today(), self.investment_date)
        return None

    interest_type = models.CharField(
        default=None,
        blank=True,
        null=True,
        max_length=50,
        choices=InterestTypes.choices,
        verbose_name="Interest Type",
    )

    prime_modifier = models.FloatField(
        default=None, blank=True, null=True, verbose_name="Prime Modifier"
    )

    expected_roi = models.FloatField(
        default=None,
        blank=True,
        null=True,
        verbose_name="Expected Return On Investment",
    )

    symbol = models.CharField(
        default=None, blank=True, null=True, max_length=10, verbose_name="Ticker Symbol"
    )

    volatility_choice = models.CharField(
        default=None,
        blank=True,
        null=True,
        choices=VolatilityChoices.choices,
        max_length=50,
        verbose_name="Volatility Choice",
    )

    def __str__(self):
        return " - ".join(("Investment", str(self.pk), str(self.name)))
