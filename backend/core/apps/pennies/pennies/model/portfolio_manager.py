import math
from typing import Dict

from pennies.model.portfolio import Portfolio


class PortfolioManager:
    """In charge of implementing a payment plan on a portfolio and incurring the monthly interest"""

    @classmethod
    def forward_on_month(
        cls, portfolio: Portfolio, payments: Dict[str, float], month: int
    ) -> Portfolio:
        forward_portfolio = portfolio.copy(deep=True)
        # if (month % 3 == 0):
        #     print(month / 3)
        #     print(forward_portfolio)
        #     print(payments)
        cls._incur_portfolio_interest(forward_portfolio, month)
        cls._implement_allocation_plan(forward_portfolio, payments, month)
        cls._remove_paid_off_loans(forward_portfolio)
        return forward_portfolio

    @classmethod
    def _implement_allocation_plan(
        cls, portfolio: Portfolio, payments: Dict[str, float], month: int
    ) -> None:
        for instrument_name, payment in payments.items():
            if payment == 0:
                continue
            instrument = portfolio.get_instrument(instrument_name)
            mmp = instrument.get_minimum_monthly_payment(month)
            if math.isclose(instrument.current_balance, 0) and not math.isclose(payment, 0) and (payment < mmp):
                print(
                    f"Payment of {payment} for {instrument_name} less than minimum monthly payment of {mmp}"
                )
            instrument.receive_payment(payment)

    @classmethod
    def _remove_paid_off_loans(cls, portfolio: Portfolio) -> None:
        paid_off_loans = [loan for loan in portfolio.loans if loan.current_balance == 0]
        for loan in paid_off_loans:
            portfolio.remove_instrument(loan.name)

    @classmethod
    def _incur_portfolio_interest(cls, portfolio: Portfolio, month: int):
        for instrument in portfolio.instruments.values():
            instrument.incur_monthly_interest(month)
