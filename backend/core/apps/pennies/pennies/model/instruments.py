# INVESTMENT_ACCOUNT = ("TFSA", "RRSP", "NonRegisteredAccount", "RESP")
# INVESTMENT_VEHICLE = (
#     "MUTUAL_FUND",
#     "GIC",
#     "TERM_DEPOSIT",
#     "ETF",
# )


# class MutualFund:
#     # created by a fund manager
#     # nav - net asset value

#     name
#     risk_tolerance  # what user thinks the risk tolerance of said mutual fund is, must be able to say i don't know
#     current_investment_balance
#     pre_authorized_contribution_amount  # annoying to change
#     contribution_frequency
#     contribution_end_date  # not sure option
#     # model decides additional contributions or to change automatic monthly contributions


# class ETF:
#     # created by a fund manager
#     # nav - net asset value

#     name
#     risk_tolerance  # what user thinks the risk tolerance of said mutual fund is, must be able to say i don't know
#     current_investment_balance
#     pre_authorized_contribution_amount  # annoying to change
#     contribution_frequency
#     contribution_end_date  # not sure option
#     # model decides additional contributions or to change automatic monthly contributions


# class GuaranteedInvestmentCertificate:
#     principal_investment_amount
#     investment_date  # date that the signed the contract (might be another word for this)
#     term_length  # months / years / days
#     maturity_date  # auto-populate based on term length
#     interest_rate  # fixed or fluctuating


# class TermDeposit:
#     principal_investment_amount
#     investment_date  # date that the signed the contract (might be another word for this)
#     term_length  # months / years
#     maturity_date  # auto-populate based on term length
#     interest_rate: FixedInterestRate


# class Stock:
#     symbol
#     amount_invested
#     expected_growth_rate  # TODO: prepopulate with industry current methods
#     # model decides additional contributions or to change automatic monthly contributions


# class Bond:
#     # check back with Aqil - kind of like a GIC
#     pass


# class CashAccount:
#     amount
#     pre_authorized_contribution_amount  # annoying to change
#     contribution_frequency
#     contribution_end_date  # not sure option
#     # model decides additional contributions or to change automatic monthly contributions
