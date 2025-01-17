<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card align="center">
      <v-col cols="12" md="10">
        <div class="text-h6">
          Tell us about your loan
        </div>
        <v-divider class="my-5" />
        <v-form ref="form">
          <v-text-field
            v-for="(textField, fieldName) in baseLoanFields"
            :key="fieldName"
            v-model="textField.value"
            class="my-1"
            outlined
            :label="textField.labelName"
            :type="textField.type"
            :rules="[v => !!v || `${getProperSentenceCapitalization(textField.labelName)} is required`, ...(textField.rules || [])]"
            :prefix="textField.prefix"
            :suffix="textField.suffix"
          />
          <v-autocomplete
            v-model="loan_type"
            label="Pick your loan type"
            solo
            outlined
            item-color="primary"
            :items="loanTypes"
          />
          <v-autocomplete
            v-model="interest_type"
            label="Pick loan interest type"
            solo
            outlined
            item-color="primary"
            :items="interestTypes"
          />
          <div v-show="showDetails">
            <v-divider class="mb-6" />
            <v-text-field
              v-if="isFixedInterestRate"
              v-model="apr"
              class="my-1"
              outlined
              label="APR"
              type="number"
              suffix="%"
              :rules="[v => !!v || 'APR is required']"
            />
            <v-text-field
              v-if="isVariableInterestRate"
              v-model="prime_modifier"
              class="my-1"
              outlined
              label="Interest Rate Relvative to Prime"
              type="number"
              suffix="%"
              :rules="[v => !!v || 'Interest Rate is required']"
            />
            <v-text-field
              v-if="isMortgage"
              v-model="current_term_end_date"
              class="my-1"
              outlined
              label="Current Term End Date"
              type="date"
              :rules="[v => !!v || 'Current term end date is required', v => new Date(v) > new Date() || 'Mortgage end date cannot be in the past']"
            />
            <v-text-field
              v-for="(textField, fieldName) in mandatoryTextFields"
              :key="fieldName"
              v-model="textField.value"
              class="my-1"
              outlined
              :label="textField.labelName"
              :type="textField.type"
              :rules="[v => !!v || `${getProperSentenceCapitalization(textField.labelName)} is required`, ...(textField.rules || [])]"
              :prefix="textField.prefix"
              :suffix="textField.suffix"
            />
          </div>
        </v-form>
        <v-card-actions class="justify-center">
          <v-btn x-large color="primary" @click.stop="createOrUpdateLoan()">
            Save Loan
          </v-btn>
        </v-card-actions>
      </v-col>
    </v-card>
  </v-dialog>
</template>

<script>
import LoanDetailsMixin from '@/mixins/LoanDetailsMixin.js'
import { calculateMinimumAmortizedLoanPayment } from '~/assets/utils.js'

export default {
  mixins: [LoanDetailsMixin],
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    modalName: {
      type: String,
      required: true
    },
    loanId: {
      type: Number,
      required: true
    }
  },
  data () {
    const loan = this.$store.getters['finances/getLoanById'](this.loanId) || {}
    // const mortgageDetails = loan.mortgage_details || {}
    const loanInterest = loan.loan_interest || {}

    const baseLoanFields = {
      name: {
        labelName: 'Loan Name',
        value: loan.name
      }
    }

    const instalmentLoanFields = {
      current_balance: {
        labelName: 'Current Balance',
        value: loan.current_balance,
        type: 'number',
        prefix: '$',
        rules: [v => v >= 0 || 'Current balance cannot be a negative number']
      },
      end_date: {
        labelName: 'Loan Due Date',
        value: loan.end_date,
        type: 'date',
        rules: [v => new Date(v) > new Date() || 'Loan due date cannot be in the past']
      },
      minimum_monthly_payment: {
        labelName: 'Minimum Monthly Payment',
        value: loan.minimum_monthly_payment,
        type: 'number',
        prefix: '$',
        rules: [
          // v => this.validateMinPayment(v) || `Minimum payment must at least ${asDollar(this.minimumMonthlyPaymentLowerBound)}`,
          v => v >= 0 || 'Minimum monthly payment cannot be a negative number'
        ]
      }
    }

    const mortgageFields = {
      current_balance: {
        labelName: 'Current Mortgage Balance',
        value: loan.current_balance,
        type: 'number',
        prefix: '$',
        rules: [v => v >= 0 || 'Current balance cannot be a negative number']
      },
      minimum_monthly_payment: {
        labelName: 'Monthly Payment',
        value: loan.miimum_monthly_payment,
        type: 'number',
        prefix: '$',
        rules: [
          // v => this.validateMinPayment(v) || `Minimum payment must at least ${asDollar(this.minimumMonthlyPaymentLowerBound)}`,
          v => v >= 0 || 'Minimum monthly payment cannot be a negative number'
        ]
      },
      end_date: {
        labelName: 'Mortgage End Date',
        value: loan.end_date,
        type: 'date',
        rules: [v => new Date(v) > new Date() || 'Mortgage end date cannot be in the past']
      }
    }

    const revolvingLoanFields = {
      current_balance: {
        labelName: 'Current Balance',
        value: loan.current_balance,
        type: 'number',
        prefix: '$',
        rules: [v => v >= 0 || 'Current balance cannot be a negative number']
      }
    }
    return {
      baseLoanFields,
      mortgageFields,
      instalmentLoanFields,
      revolvingLoanFields,
      id: loan.id,
      interest_type: loanInterest.interest_type, // needed for mixin
      loan_type: loan.loan_type, // needed for mixin
      loanName: loan.name,
      apr: loanInterest.apr,
      prime_modifier: loanInterest.prime_modifier,
      current_term_end_date: loanInterest.current_term_end_date
    }
  },
  computed: {
    // booleans
    showDetails () {
      return this.interest_type !== null & this.loan_type !== null
    },

    mandatoryTextFields () {
      if (this.isInstalmentLoan) {
        return this.instalmentLoanFields
      } else if (this.isRevolvingLoan) {
        return this.revolvingLoanFields
      } else if (this.isMortgage) {
        return this.mortgageFields
      } else {
        return {}
      }
    },

    // loan properties
    interestType () {
      return this.interest_type
    },
    loanType () {
      return this.loan_type
    },
    minimumMonthlyPayment () {
      if (this.isInstalmentLoan) {
        return this.instalmentLoanFields.minimum_monthly_payment.value
      } else if (this.isMortgage) {
        return this.mortgageFields.monthly_payment.value
      } else {
        return null
      }
    },
    endDate () {
      if (this.isInstalmentLoan) {
        return new Date(this.instalmentLoanFields.end_date.value)
      } else {
        return null
      }
    },
    currentBalance () {
      if (this.isInstalmentLoan) {
        return this.instalmentLoanFields.current_balance.value
      } else if (this.isRevolvingLoan) {
        return this.revolvingLoanFields.current_balance.value
      } else {
        return null
      }
    },
    mortgageStartDate () {
      return this.isMortgage ? new Date(this.mortgageFields.purchase_date.value) : null
    },
    currentMortgageTermStartDate () {
      return this.isMortgage ? new Date(this.mortgageFields.current_term_start_date.value) : null
    },
    mortgageLength () {
      return this.isMortgage ? this.mortgageFields.amortization_years.value : null
    },
    currentMortgageTermLength () {
      return this.isMortgage ? this.mortgageFields.current_term_years.value : null
    },
    mortgagePurchasePrice () {
      return this.isMortgage ? this.mortgageFields.purchase_price.value : null
    },

    effectiveInterestRate () {
      return this.isFixedInterestRate ? this.apr : this.currentPrimeRatePercent + Number(this.prime_modifier)
    },
    minimumMonthlyPaymentLowerBound () {
      if (this.isInstalmentLoan) {
        if (!this.endDate || this.endDate <= new Date()) {
          return null
        }
        return calculateMinimumAmortizedLoanPayment(
          this.currentBalance,
          this.effectiveInterestRate,
          this.endDate
        )
      } else if (this.isMortgage) {
        return null
      } else {
        return null
      }
    },

    // dialog functionality
    show: {
      get () {
        return this.visible
      },
      set (value) {
        if (!value) {
          this.$emit('close')
        }
      }
    }
  },
  methods: {
    createOrUpdateLoan () {
      const isValidLoan = this.validateLoan()
      if (!isValidLoan) {
        return // don't submit if does not pass validation or contain error
      }
      this.show = false
      this.$store.dispatch('finances/createOrUpdateLoan', this.makeLoanObject())
    },
    validateLoan () {
      const isValidForm = this.$refs.form.validate()
      return isValidForm & !this.minimumMonthlyPaymentErrorMessage
    },
    makeLoanObject () {
      const loan = Object()
      for (const [fieldName, object] of Object.entries(this.mandatoryTextFields)) {
        loan[fieldName] = object.value
      }
      for (const [fieldName, object] of Object.entries(this.baseLoanFields)) {
        loan[fieldName] = object.value
      }
      loan.loan_interest = this.makeLoanInterestObject()
      loan.loan_type = this.loan_type
      loan.id = this.id
      return loan
    },
    makeLoanInterestObject () {
      const loanInterst = {}
      if (this.isFixedInterestRate) {
        loanInterst.interest_type = this.interest_type
        loanInterst.apr = this.apr
      } else if (this.isVariableInterestRate) {
        loanInterst.interest_type = this.interest_type
        loanInterst.prime_modifier = this.prime_modifier
      }
      if (this.isMortgage) {
        loanInterst.current_term_end_date = this.current_term_end_date
      }
      return loanInterst
    },
    validateMinPayment (v) {
      if (v && this.isInstalmentLoan) {
        return v >= v.minimumMonthlyPaymentLowerBound
      } else {
        return true
      }
    },
    getProperSentenceCapitalization (s) {
      return s[0].toUpperCase() + s.substring(1).toLowerCase()
    },
    getDatePlusYears (startDate, numYears) {
      if (startDate && numYears) {
        const d = new Date(startDate)
        d.setFullYear(Number(startDate.getFullYear()) + Number(numYears))
        return d
      } else {
        return null
      }
    }
  }
}
</script>
