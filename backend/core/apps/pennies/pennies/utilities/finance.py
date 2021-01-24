from pennies.model.loan import Loan


def get_interest_paid_on_loan(loan: Loan, months: int):
    return abs(
        loan.current_balance * (1 + loan.monthly_interest_rate) ** months
        - loan.current_balance
    )
