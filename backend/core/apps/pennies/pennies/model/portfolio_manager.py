from typing import Dict

from pennies.model.portfolio import Portfolio


class PortfolioManager:
    """In charge of implementing a payment plan on a portfolio and incurring the monthly interest"""

    @classmethod
    def forward_on_month(cls, portfolio: Portfolio, payments: Dict[str, float]) -> None:
        cls._incur_portfolio_interest(portfolio)
        cls._implement_allocation_plan(portfolio, payments)
        cls._remove_paid_off_loans(portfolio)

    @classmethod
    def _implement_allocation_plan(cls, portfolio: Portfolio, payments: Dict[str, float]) -> None:
        for instrument_name, payment in payments.items():
            if payment == 0:
                continue
            portfolio.get_instrument(instrument_name).receive_payment(payment)

    @classmethod
    def _remove_paid_off_loans(cls, portfolio: Portfolio) -> None:
        paid_off_loans = [loan for loan in portfolio.loans if loan.current_balance == 0]
        for loan in paid_off_loans:
            portfolio.remove_instrument(loan.name)

    @classmethod
    def _incur_portfolio_interest(cls, portfolio: Portfolio):
        for instrument in portfolio.instruments.values():
            instrument.incur_monthly_interest()
