class TFSALimitGetter:

    FUTURE_TFSA_LIMIT = 6000
    HISTORICAL_TFSA_LIMITS = {
        2009: 5000,
        2010: 5000,
        2011: 5000,
        2012: 5000,
        2013: 5500,
        2014: 5500,
        2015: 10_000,
        2016: 5500,
        2017: 5500,
        2018: 5500,
        2019: 6000,
        2020: 6000
    }

    @classmethod
    def get_limit(cls, year: int):
        if year < min(cls.HISTORICAL_TFSA_LIMITS.keys()):
            return 0
        elif year > max(cls.HISTORICAL_TFSA_LIMITS.keys()):
            return cls.FUTURE_TFSA_LIMIT
        else:
            return cls.HISTORICAL_TFSA_LIMITS[year]
