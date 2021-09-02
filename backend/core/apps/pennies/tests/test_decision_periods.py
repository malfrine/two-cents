from pennies.model.decision_periods import (
    DecisionPeriodsManager,
    DecisionPeriodsManagerFactory,
    WorkingPeriod,
    RetirementPeriod,
    make_grouped_months_from_events,
)
from pennies.utilities.datetime import DateTimeHelper


def test_decision_periods():
    dt_helper = DateTimeHelper.create(3, 19)
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
        dt_helper=dt_helper,
    )

    test_phs = DecisionPeriodsManagerFactory(max_months=3).from_num_months(
        start_month=3, retirement_month=13, final_month=20
    )

    for actual, test in zip(actual_phs.data, test_phs.data):
        assert actual.months == test.months
        assert actual.index == test.index


def test_month_grouping():
    max_months = 24
    sorted_events = [(0, False), (11, True), (40, False), (70, True), (90, False)]
    grouped_months = make_grouped_months_from_events(
        sorted_events=sorted_events, max_months=max_months
    )
    actual_months = [
        list(range(0, 11)),
        [11],
        list(range(12, 12 + max_months)),
        list(range(36, 40)),
        list(range(40, 40 + max_months)),
        list(range(64, 70)),
        [70],
        list(range(71, 90)),
    ]
    assert len(actual_months) == len(grouped_months)
    for group in grouped_months:
        assert len(group) <= max_months
    for group, actual in zip(grouped_months, actual_months):
        assert group == actual
