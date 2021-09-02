import math
from typing import List

from pennies.model import taxes
from pennies.model.constants import Province, InvestmentAccountType
from pennies.model.instrument import Instrument
from pennies.model.investment import BaseInvestment
from pennies.model.taxes import (
    PROVINCIAL_TAX_MAP,
    IncomeTaxBrackets,
    CAPITAL_GAINS_TAX_FRACTION,
)
from pennies.utilities.datetime import MONTHS_IN_YEAR


class LoanMinimumPaymentCalculator:
    @classmethod
    def calculate_for_instalment_loan(
        cls, principal: float, apr: float, num_months: int
    ):
        mir = cls.calculate_monthly_interest_rate(apr)
        top = mir * (1 + mir) ** num_months
        bottom = (1 + mir) ** num_months - 1
        discount_factor = top / bottom
        return math.floor(principal * discount_factor)

    @classmethod
    def calculate_for_revolving_loan(cls, principal: float, apr: float):
        return math.floor(principal * cls.calculate_monthly_interest_rate(apr))

    @classmethod
    def calculate_monthly_interest_rate(cls, apr):
        return apr / MONTHS_IN_YEAR / 100


def calculate_loan_ending_payment(current_balance, interest_rate, num_months) -> float:
    if interest_rate == 0:
        return current_balance / num_months
    compounded_rate = (1 + interest_rate) ** num_months
    return current_balance * interest_rate * compounded_rate / (compounded_rate - 1)


def calculate_average_monthly_interest_rate(instrument: Instrument, months: List[int]):
    return sum(instrument.monthly_interest_rate(month) for month in months) / len(
        months
    )


def calculate_balance_after_fixed_monthly_payments(
    instrument, monthly_payment, months: List[int]
):
    r = calculate_average_monthly_interest_rate(instrument, months)
    n = len(months)
    return (
        instrument.current_balance * (1 + r) ** n
        + monthly_payment * ((1 + r) ** n - 1) / r
    )


def calculate_annual_income_tax_from_brackets(
    income: float, brackets: IncomeTaxBrackets
):
    tax = 0
    rem_income = income
    for bracket in brackets.data:
        taxable_income_in_bracket = min(rem_income, bracket.marginal_upper_bound)
        tax += taxable_income_in_bracket * bracket.marginal_tax_rate_as_fraction
        rem_income -= taxable_income_in_bracket
        if rem_income == 0:
            return tax
    raise ValueError(f"Could not calculate income taxes for {income} using {brackets}")


def calculate_monthly_income_tax_from_brackets(
    income: float, brackets: IncomeTaxBrackets
):
    tax = 0
    rem_income = income
    for bracket in brackets.data:
        taxable_income_in_bracket = min(
            rem_income, bracket.monthly_marginal_upper_bound
        )
        tax += taxable_income_in_bracket * bracket.marginal_tax_rate_as_fraction
        rem_income -= taxable_income_in_bracket
        if rem_income == 0:
            return tax
    raise ValueError(f"Could not calculate income taxes for {income} using {brackets}")


def calculate_annual_income_tax(income: float, province: Province):
    prov_tax = calculate_annual_income_tax_from_brackets(
        income, PROVINCIAL_TAX_MAP[province]
    )
    fed_tax = calculate_annual_income_tax_from_brackets(income, taxes.FEDERAL)
    return prov_tax + fed_tax


def calculate_monthly_income_tax(income: float, province: Province):
    prov_tax = calculate_monthly_income_tax_from_brackets(
        income, PROVINCIAL_TAX_MAP[province]
    )
    fed_tax = calculate_monthly_income_tax_from_brackets(income, taxes.FEDERAL)
    return prov_tax + fed_tax


def calculate_instrument_balance(
    cur_balance, num_months, growth_rate, withdrawal, allocation
):
    """not type hinted because this can be used for pyomo constraints"""
    if num_months < 0:
        raise ValueError(f"Number of months cannot be negative: {num_months}")
    elif growth_rate < -0.01:
        raise ValueError(f"Growth rate cannot be negative: {growth_rate}")

    r = 1 + growth_rate
    if num_months == 0:
        return cur_balance

    elif r == 1:
        return cur_balance + (allocation - withdrawal) * num_months
    else:
        balance_growth = cur_balance * r ** num_months
        allocation_growth = (allocation - withdrawal) * (r ** num_months - 1) / (r - 1)

        return balance_growth + allocation_growth


def estimate_taxable_withdrawal(
    investment: BaseInvestment, withdrawal, months: List[int]
):
    """
    This isn't the correct way to calculate capital gains but it's an okay estimation based on the investment lifetime
    Previous withdrawals and allocations need to be considered

    For RRSPs and TFSAs, this is correct
    But for Non-registered the ACB (adjusted cost base) is needed - introducing ACB makes the calculation non-linear
    and not suitable for MILPs
    """
    if investment.account_type == InvestmentAccountType.RRSP:
        # RRSP withdrawals are fully taxed
        return withdrawal
    elif investment.account_type == InvestmentAccountType.TFSA:
        return 0
    else:  # non-registered investment
        # estimate based on average interest rate and decision period
        # can't actually calculate this because of non-linear nature of capital gains calculation
        estimated_total_return_rate = 1
        for month in months:
            estimated_total_return_rate *= 1 + investment.monthly_interest_rate(month)
        if estimated_total_return_rate <= 0:
            # TODO: there could be tax write-offs for investments that lose money
            # but hard to estimate
            return 0
        else:
            capital_gains_fraction = (
                estimated_total_return_rate - 1
            ) / estimated_total_return_rate
            return withdrawal * capital_gains_fraction * CAPITAL_GAINS_TAX_FRACTION
