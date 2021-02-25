import math
from typing import List

from pennies.model import taxes
from pennies.model.constants import Province
from pennies.model.instrument import Instrument
from pennies.model.taxes import PROVINCIAL_TAX_MAP, IncomeTaxBrackets, FEDERAL
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
        return current_balance
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


def calculate_annual_income_tax_from_brackets(income: float, brackets: IncomeTaxBrackets):
    tax = 0
    rem_income = income
    for bracket in brackets.data:
        taxable_income_in_bracket = min(rem_income, bracket.marginal_upper_bound)
        tax += taxable_income_in_bracket * bracket.marginal_tax_rate_as_fraction
        rem_income -= taxable_income_in_bracket
        if rem_income == 0:
            return tax
    raise ValueError(f"Could not calculate income taxes for {income} using {brackets}")


def calculate_monthly_income_tax_from_brackets(income: float, brackets: IncomeTaxBrackets):
    tax = 0
    rem_income = income
    for bracket in brackets.data:
        taxable_income_in_bracket = min(rem_income, bracket.monthly_marginal_upper_bound)
        tax += taxable_income_in_bracket * bracket.marginal_tax_rate_as_fraction
        rem_income -= taxable_income_in_bracket
        if rem_income == 0:
            return tax
    raise ValueError(f"Could not calculate income taxes for {income} using {brackets}")


def calculate_annual_income_tax(income: float, province: Province):
    prov_tax = calculate_annual_income_tax_from_brackets(income, PROVINCIAL_TAX_MAP[province])
    fed_tax = calculate_annual_income_tax_from_brackets(income, taxes.FEDERAL)
    return prov_tax + fed_tax


def calculate_monthly_income_tax(income: float, province: Province):
    prov_tax = calculate_monthly_income_tax_from_brackets(income, PROVINCIAL_TAX_MAP[province])
    fed_tax = calculate_monthly_income_tax_from_brackets(income, taxes.FEDERAL)
    return prov_tax + fed_tax
