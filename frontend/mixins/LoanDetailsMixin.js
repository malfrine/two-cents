export default {
  data () {
    return {
      mortgageTypeLabel: 'Mortgage',
      fixedInterestRateLabel: 'Fixed',
      variableInterestRateLabel: 'Variable',
      loanTypes: ['Mortgage', 'Student Line of Credit', 'Line of Credit', 'Credit Card', 'Student Loan', 'Car Loan', 'Personal Loan'],
      interestTypes: ['Fixed', 'Variable'],
      revolvingLoans: ['Student Line of Credit', 'Line of Credit', 'Credit Card'],
      instalmentLoans: ['Student Loan', 'Car Loan', 'Personal Loan'],
      minMinimumPaymentThreshold: 10,
      currentPrimeRatePercent: 2.5
    }
  },
  computed: {
    loanType () {
      return '' // needs to be overwritten
    },
    interestType () {
      return '' // needs to be overwritten
    },
    isMortgage () {
      return this.loanType === this.mortgageTypeLabel
    },
    isRevolvingLoan () {
      return this.revolvingLoans.includes(this.loanType)
    },
    isInstalmentLoan () {
      return this.instalmentLoans.includes(this.loanType)
    },
    isFixedInterestRate () {
      return this.interestType === this.fixedInterestRateLabel
    },
    isVariableInterestRate () {
      return this.interestType === this.variableInterestRateLabel
    }
  }
}
