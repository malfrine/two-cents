from pennies.model.decision_periods import (
    DecisionPeriod,
    DecisionPeriodsManager,
    DecisionPeriodsManagerFactory,
    WorkingPeriod,
    RetirementPeriod,
)
from pennies.utilities.datetime import DateTimeHelper


def test_decision_periods():
    dt_helper = DateTimeHelper.create(19)
    actual_phs = DecisionPeriodsManager(
        data=[
            WorkingPeriod(index=0, months=[3, 4, 5]),
            WorkingPeriod(index=1, months=[6, 7, 8]),
            WorkingPeriod(index=2, months=[9, 10, 11]),
            WorkingPeriod(index=3, months=[12]),
            RetirementPeriod(index=4, months=[13, 14, 15]),
            RetirementPeriod(index=5, months=[16, 17, 18]),
            RetirementPeriod(index=6, months=[19]),
        ],
        dt_helper=dt_helper
    )

    test_phs = DecisionPeriodsManagerFactory(max_months=3).from_num_months(
        start_month=3, retirement_month=13, final_month=20
    )

    for actual, test in zip(actual_phs.data, test_phs.data):
        assert actual.months == test.months
        assert actual.index == test.index
