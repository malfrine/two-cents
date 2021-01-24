from datetime import datetime, date
from typing import List

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel

from pennies.model.solution import FinancialPlan, MonthlySolution
from pennies.utilities.datetime import get_first_date_of_next_month

_SAMPLE_RATE = 6  # months


class InstrumentForecast(BaseModel):
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
            cur_date + relativedelta(months=index * _SAMPLE_RATE)
            for index in range(len(monthly_solutions))
        )

    @classmethod
    def _get_instrument_forecasts(
        cls, monthly_solutions: List[MonthlySolution]
    ) -> List[InstrumentForecast]:

        if len(monthly_solutions) == 0:
            return list()

        def get_instrument_balance_or_zero(instrument_name: str, ms: MonthlySolution):
            instrument = ms.portfolio.instruments.get(instrument_name, None)
            if instrument is None:
                return 0
            else:
                return round(instrument.current_balance)

        all_instruments = list(monthly_solutions[0].portfolio.instruments.keys())
        return [
            InstrumentForecast(
                label=instrument_name,
                data=[
                    get_instrument_balance_or_zero(instrument_name, ms)
                    for ms in monthly_solutions
                ],
            )
            for instrument_name in all_instruments
        ]
