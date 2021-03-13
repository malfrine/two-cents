from math import isclose

from pennies.model.taxes import TaxBracket, IncomeTaxBrackets
from pennies.utilities.finance import (
    calculate_annual_income_tax,
    calculate_annual_income_tax_from_brackets,
    calculate_monthly_income_tax_from_brackets,
)


def make_simple_brackets():
    return IncomeTaxBrackets(
        data=[
            TaxBracket(marginal_upper_bound=50, marginal_tax_rate=10),
            TaxBracket(marginal_upper_bound=100, marginal_tax_rate=20),
        ]
    )


def test_simple_tax_brackets():
    test_brackets = make_simple_brackets()
    assert calculate_annual_income_tax_from_brackets(0, test_brackets) == 0
    assert calculate_annual_income_tax_from_brackets(49, test_brackets) == 49 * 0.1
    assert (
        calculate_annual_income_tax_from_brackets(51, test_brackets)
        == 50 * 0.1 + 1 * 0.2
    )
    assert (
        calculate_annual_income_tax_from_brackets(100, test_brackets)
        == 50 * 0.1 + 50 * 0.2
    )

    assert isclose(
        calculate_monthly_income_tax_from_brackets(0 / 12, test_brackets), 0 / 12
    )
    assert isclose(
        calculate_monthly_income_tax_from_brackets(49 / 12, test_brackets),
        49 * 0.1 / 12,
    )
    assert isclose(
        calculate_monthly_income_tax_from_brackets(51 / 12, test_brackets),
        (50 * 0.1 + 1 * 0.2) / 12,
    )
    assert isclose(
        calculate_monthly_income_tax_from_brackets(100 / 12, test_brackets),
        (50 * 0.1 + 50 * 0.2) / 12,
    )


def test_cumulative_incomes():
    test_brackets = make_simple_brackets()
    assert test_brackets.get_bracket_cumulative_income(0) == 50
    assert test_brackets.get_bracket_cumulative_income(1) == 150
