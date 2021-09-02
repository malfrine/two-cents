from typing import Dict

RRSP_LIMIT_INCOME_FACTOR = 0.18


def make_rrsp_historical_limits() -> Dict[int, float]:
    """
    https://www.canada.ca/en/revenue-agency/services/tax/registered-plans-administrators/pspa/mp-rrsp-dpsp-tfsa-limits-ympe.html
    """
    return {
        2022: 29_210,
        2021: 27_830,
        2020: 27_230,
        2019: 26_500,
        2018: 26_230,
        2017: 26_010,
        2016: 25_370,
        2015: 24_930,
        2014: 24_270,
        2013: 23_820,
        2012: 22_970,
        2011: 22_450,
        2010: 22_000,
        2009: 21_000,
        2008: 20_000,
        2007: 19_000,
        2006: 18_000,
        2005: 16_500,
        2004: 15_500,
        2003: 14_500,
        2002: 13_500,
        2001: 13_500,
        2000: 13_500,
        1999: 13_500,
        1998: 13_500,
        1997: 13_500,
        1996: 13_500,
        1995: 14_500,
        1994: 13_500,
        1993: 12_500,
        1992: 12_500,
        1991: 11_500,
    }


def make_rrif_min_payments_by_age():
    """
    https://www.canada.ca/en/revenue-agency/services/tax/businesses/topics/completing-slips-summaries/t4rsp-t4rif-information-returns/payments/chart-prescribed-factors.html#nt_2
    as of march 12, 2021
    """
    return {
        71: 5.28,
        72: 5.40,
        73: 5.53,
        74: 5.67,
        75: 5.82,
        76: 5.98,
        77: 6.17,
        78: 6.36,
        79: 6.58,
        80: 6.82,
        81: 7.08,
        82: 7.38,
        83: 7.71,
        84: 8.08,
        85: 8.51,
        86: 8.99,
        87: 9.55,
        88: 10.21,
        89: 10.99,
        90: 11.92,
        91: 13.06,
        92: 14.49,
        93: 16.34,
        94: 18.79,
    }


class RRSPAnnualLimitGetter:
    DEFAULT_FUTURE_LIMIT = 25_000
    DEFAULT_PAST_LIMIT = 10_000
    CUTOFF_YEAR = 1991
    HISTORICAL_LIMITS = make_rrsp_historical_limits()

    @classmethod
    def get_limit(cls, year: int):
        return cls.HISTORICAL_LIMITS.get(year, None) or (
            cls.DEFAULT_PAST_LIMIT
            if year < cls.CUTOFF_YEAR
            else cls.DEFAULT_FUTURE_LIMIT
        )


class RRIFMinPaymentCalculator:
    DENOMINATOR_AGE = 90
    RRIF_PAYMENTS_BY_AGE = make_rrif_min_payments_by_age()

    @classmethod
    def get_min_payment_percentage(cls, age: int):
        min_percentage = cls.RRIF_PAYMENTS_BY_AGE.get(age, None)
        if min_percentage is not None:
            return min_percentage
        elif age > max(cls.RRIF_PAYMENTS_BY_AGE.keys()):
            return 20
        else:
            return max(0, 1 / (1 - cls.DENOMINATOR_AGE) * 100)
