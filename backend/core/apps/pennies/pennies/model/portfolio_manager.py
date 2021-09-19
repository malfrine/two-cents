import logging
import math
from typing import Dict

from pennies.model.instrument import Instrument
from pennies.model.investment import GuaranteedInvestment, NonGuaranteedInvestment
from pennies.model.loan import Loan, RevolvingLoan
from pennies.model.portfolio import Portfolio
from pennies.utilities.dict import remove_from_dict


class PortfolioManager:
    """In charge of implementing a payment plan on a portfolio and incurring the monthly interest"""

    @classmethod
    def forward_on_month(
        cls,
        portfolio: Portfolio,
        payments: Dict[str, float],
        month: int,
        withdrawals: Dict[str, float] = None,
    ) -> None:
        if withdrawals is None:
            withdrawals = dict()
        cls._incur_portfolio_interest(portfolio, month)
        cls._implement_allocation_plan(portfolio, payments, month)
        cls._implement_withdrawals(portfolio, withdrawals, month)
        cls._remove_paid_off_loans(portfolio)

    @classmethod
    def _implement_allocation_plan(
        cls, portfolio: Portfolio, payments: Dict[str, float], month: int
    ) -> None:
        for instrument_name, payment in payments.items():
            if math.isclose(payment, 0, abs_tol=0.01):
                continue
            try:
                instrument = portfolio.get_instrument(instrument_name)
            except KeyError:
                print(
                    f"Unable to find {instrument} in portfolio - skipping payment of {payment} in month: {month}"
                )
                continue
            mmp = instrument.get_minimum_monthly_payment(month)
            if (
                math.isclose(instrument.current_balance, 0)
                and not math.isclose(payment, 0)
                and (payment < mmp)
            ):
                logging.warning(
                    f"Payment of {payment} for {instrument_name} less than minimum monthly payment of {mmp}"
                )
            cls._execute_payment(instrument, payment)

    @classmethod
    def _remove_paid_off_loans(cls, portfolio: Portfolio) -> None:
        paid_off_loans = [loan for loan in portfolio.loans if loan.is_paid_off()]
        for loan in paid_off_loans:
            remove_from_dict(loan.id_, portfolio.instruments)

    @classmethod
    def _incur_portfolio_interest(cls, portfolio: Portfolio, month: int):
        for instrument in portfolio.instruments.values():
            cls._incur_instrument_interest(instrument, month)

    @classmethod
    def _execute_payment(cls, instrument: Instrument, payment: float):
        if isinstance(instrument, Loan):
            if payment >= abs(instrument.current_balance):
                instrument.current_balance = 0
            else:
                instrument.current_balance += payment
        elif isinstance(instrument, GuaranteedInvestment):
            raise ValueError("Cannot execute payments for guaranteed investments")
        elif isinstance(instrument, Instrument):
            instrument.current_balance += payment
        else:
            raise ValueError("Unknown instrument type")

    @classmethod
    def _incur_instrument_interest(cls, instrument: Instrument, month: int):
        if (
            isinstance(instrument, GuaranteedInvestment)
            and month > instrument.final_month
        ):
            return
        instrument.current_balance += (
            instrument.current_balance * instrument.monthly_interest_rate(month)
        )

    @classmethod
    def _implement_withdrawals(
        cls, portfolio: Portfolio, withdrawals: Dict[str, float], month: int
    ):
        for instrument_name, withdrawal_amount in withdrawals.items():
            instrument = portfolio.get_instrument(instrument_name)
            if withdrawal_amount == 0:
                continue
            cls._execute_withdrawal(instrument, withdrawal_amount, month)

    @classmethod
    def _execute_withdrawal(
        cls, instrument: Instrument, withdrawal_amount: float, month: int
    ):
        if isinstance(instrument, RevolvingLoan):
            instrument.current_balance -= withdrawal_amount
            # TODO: add withdrawal limit
        elif isinstance(instrument, NonGuaranteedInvestment):
            instrument.current_balance -= withdrawal_amount
        elif isinstance(instrument, GuaranteedInvestment):
            if month >= instrument.final_month:
                instrument.current_balance -= withdrawal_amount
            else:
                raise ValueError(
                    "Cannot withdraw from a guaranteed investment that has not matured"
                )
        else:
            raise ValueError(
                f"Unable to withdraw from instrument {instrument.id_} - don't know how"
            )
