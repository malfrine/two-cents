from datetime import datetime, date
from typing import List
from uuid import UUID

from pydantic import BaseModel

from pennies.model.loan import Loan
from pennies.model.solution import FinancialPlan, MonthlySolution
from pennies.utilities.datetime import get_first_date_of_next_month, get_date_plus_month

_SAMPLE_RATE = 6  # months


class InstrumentForecast(BaseModel):
    instrument_id: int
    instrument_type: str
    label: str
    data: List[float]


class NetWorthForecast(BaseModel):
    datasets: List[InstrumentForecast]
    labels: List[date]


class NetWorthForecastFactory:
    @classmethod
    def from_plan(cls, plan: FinancialPlan) -> NetWorthForecast:

        sampled_monthly_solutions = list(
            ms for i, ms in enumerate(plan.monthly_solutions) if i % _SAMPLE_RATE == 0
        )

        return NetWorthForecast(
            datasets=cls._get_instrument_forecasts(sampled_monthly_solutions),
            labels=cls._get_all_datetime(sampled_monthly_solutions),
        )

    @classmethod
    def _get_all_datetime(cls, monthly_solutions: List[MonthlySolution]) -> List[date]:
        cur_date: date = get_first_date_of_next_month(datetime.today())
        return list(
            get_date_plus_month(cur_date, index * _SAMPLE_RATE)
            for index in range(len(monthly_solutions))
        )

    @classmethod
    def _get_instrument_forecasts(
        cls, monthly_solutions: List[MonthlySolution]
    ) -> List[InstrumentForecast]:

        if len(monthly_solutions) == 0:
            return list()

        def get_instrument_balance_or_zero(id_: UUID, ms: MonthlySolution):
            instrument = ms.portfolio.instruments.get(id_, None)
            if instrument is None:
                return 0
            else:
                return round(instrument.current_balance)

        instruments = list(monthly_solutions[0].portfolio.instruments.values())
        return [
            InstrumentForecast(
                instrument_id=instrument.db_id,
                instrument_type="loan"
                if isinstance(instrument, Loan)
                else "investment",
                label=instrument.name,
                data=[
                    get_instrument_balance_or_zero(instrument.id_, ms)
                    for ms in monthly_solutions
                ],
            )
            for instrument in instruments
        ]
