from typing import List, Dict

from pydantic.main import BaseModel

from pennies.model.constants import Province
from pennies.utilities.datetime import MONTHS_IN_YEAR

MAX_MARGINAL_ANNUAL_INCOME = 1_000_000


class TaxBracket(BaseModel):
    marginal_upper_bound: float
    marginal_tax_rate: float

    @property
    def monthly_marginal_upper_bound(self):
        return self.marginal_upper_bound / MONTHS_IN_YEAR

    @property
    def marginal_tax_rate_as_fraction(self):
        return self.marginal_tax_rate / 100


class IncomeTaxBrackets(BaseModel):
    data: List[TaxBracket]
    _cumulative_incomes: List[float] = None

    @property
    def num_brackets(self):
        return len(self.data)

    def get_bracket_cumulative_income(self, bracket_index: int):
        if self._cumulative_incomes is None:
            cumulative_incomes = list()
            cur_income = 0
            for bracket in self.data:
                cur_income += bracket.marginal_upper_bound
                cumulative_incomes.append(cur_income)
            self._cumulative_incomes = cumulative_incomes
        return self._cumulative_incomes[bracket_index]

    class Config:
        underscore_attrs_are_private = True




FEDERAL = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=49_020, marginal_tax_rate=15),
        TaxBracket(marginal_upper_bound=49_020, marginal_tax_rate=20.5),
        TaxBracket(marginal_upper_bound=53_939, marginal_tax_rate=26),
        TaxBracket(marginal_upper_bound=64_533, marginal_tax_rate=29),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=33
        ),
    ]
)

NL = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=37_929, marginal_tax_rate=8.7),
        TaxBracket(marginal_upper_bound=37_929, marginal_tax_rate=14.5),
        TaxBracket(marginal_upper_bound=59_574, marginal_tax_rate=15.8),
        TaxBracket(marginal_upper_bound=54_172, marginal_tax_rate=17.3),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=18.3
        ),
    ]
)

PEI = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=31_984, marginal_tax_rate=9.8),
        TaxBracket(marginal_upper_bound=31_985, marginal_tax_rate=13.8),
        TaxBracket(marginal_upper_bound=63_969, marginal_tax_rate=16.7),
    ]
)

NS = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=29_590, marginal_tax_rate=8.79),
        TaxBracket(marginal_upper_bound=29_590, marginal_tax_rate=14.95),
        TaxBracket(marginal_upper_bound=33_820, marginal_tax_rate=16.67),
        TaxBracket(marginal_upper_bound=57_000, marginal_tax_rate=17.5),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=21
        ),
    ]
)

NB = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=43_401, marginal_tax_rate=9.68),
        TaxBracket(marginal_upper_bound=43_402, marginal_tax_rate=14.82),
        TaxBracket(marginal_upper_bound=54_319, marginal_tax_rate=16.52),
        TaxBracket(marginal_upper_bound=59_654, marginal_tax_rate=17.84),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=20.3
        ),
    ]
)

QB = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=44_545, marginal_tax_rate=15),
        TaxBracket(marginal_upper_bound=37_929, marginal_tax_rate=14.5),
        TaxBracket(marginal_upper_bound=59_574, marginal_tax_rate=15.8),
        TaxBracket(marginal_upper_bound=54_172, marginal_tax_rate=17.3),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=18.3
        ),
    ]
)

ON = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=45_142, marginal_tax_rate=5.05),
        TaxBracket(marginal_upper_bound=45_145, marginal_tax_rate=9.15),
        TaxBracket(marginal_upper_bound=59_713, marginal_tax_rate=11.16),
        TaxBracket(marginal_upper_bound=70_00, marginal_tax_rate=12.16),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=13.16
        ),
    ]
)

MB = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=33_723, marginal_tax_rate=10.8),
        TaxBracket(marginal_upper_bound=39_162, marginal_tax_rate=12.75),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=17.4
        ),
    ]
)

SK = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=45_677, marginal_tax_rate=10.5),
        TaxBracket(marginal_upper_bound=84_829, marginal_tax_rate=12.5),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=14.5
        ),
    ]
)

AB = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=131_220, marginal_tax_rate=10),
        TaxBracket(marginal_upper_bound=26_244, marginal_tax_rate=12),
        TaxBracket(marginal_upper_bound=52_488, marginal_tax_rate=13),
        TaxBracket(marginal_upper_bound=104_976, marginal_tax_rate=14),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=15
        ),
    ]
)

BC = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=42_184, marginal_tax_rate=5.06),
        TaxBracket(marginal_upper_bound=42_185, marginal_tax_rate=7.7),
        TaxBracket(marginal_upper_bound=12_497, marginal_tax_rate=10.5),
        TaxBracket(marginal_upper_bound=20_757, marginal_tax_rate=12.29),
        TaxBracket(marginal_upper_bound=41_860, marginal_tax_rate=14.7),
        TaxBracket(marginal_upper_bound=62_937, marginal_tax_rate=16.8),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=20.5
        ),
    ]
)

YK = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=49_020, marginal_tax_rate=6.4),
        TaxBracket(marginal_upper_bound=49_020, marginal_tax_rate=9),
        TaxBracket(marginal_upper_bound=55_938, marginal_tax_rate=10.9),
        TaxBracket(marginal_upper_bound=348_022, marginal_tax_rate=12.8),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=15
        ),
    ]
)

NWT = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=44_396, marginal_tax_rate=5.9),
        TaxBracket(marginal_upper_bound=44_400, marginal_tax_rate=8.6),
        TaxBracket(marginal_upper_bound=55_566, marginal_tax_rate=12.2),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=14.05
        ),
    ]
)

NT = IncomeTaxBrackets(
    data=[
        TaxBracket(marginal_upper_bound=46_740, marginal_tax_rate=4),
        TaxBracket(marginal_upper_bound=46_740, marginal_tax_rate=7),
        TaxBracket(marginal_upper_bound=58_498, marginal_tax_rate=9),
        TaxBracket(
            marginal_upper_bound=MAX_MARGINAL_ANNUAL_INCOME, marginal_tax_rate=11.5
        ),
    ]
)


def make_provincial_tax_map() -> Dict[Province, IncomeTaxBrackets]:
    return {
        Province.NL: NL,
        Province.PEI: PEI,
        Province.NS: NS,
        Province.NB: NB,
        Province.QB: QB,
        Province.ON: ON,
        Province.MB: MB,
        Province.SK: SK,
        Province.AB: AB,
        Province.BC: BC,
        Province.YK: YK,
        Province.NWT: NWT,
        Province.NT: NT
    }


PROVINCIAL_TAX_MAP = make_provincial_tax_map()
