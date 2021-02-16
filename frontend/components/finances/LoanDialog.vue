<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card align="center">
      <v-col cols="12" md="10">
        <div class="text-h6">
          Tell us about your loan
        </div>
        <v-divider class="my-5" />
        <v-form ref="form">
          <v-select
            v-model="loan_type"
            label="Pick your loan type"
            solo
            outlined
            item-color="primary"
            :items="loanTypes"
          />
          <v-select
            v-model="interest_type"
            label="Pick loan interest type"
            solo
            outlined
            item-color="primary"
            :items="interestTypes"
          />
          <v-divider class="my-5" />
          <div v-show="showDetails">
            <v-text-field
              v-model="name"
              label="Loan Name"
              outlined
              :rules="[v => !!v || 'Must provide loan name']"
            />
            <v-text-field
              v-model="current_balance"
              label="Current Balance"
              prefix="$"
              outlined
              :rules="[v => !!v || 'Must provide loan balance']"
            />
            <v-text-field
              v-if="isFixed"
              v-model="apr"
              label="APR"
              suffix="%"
              outlined
              :rules="aprRules"
            />
            <v-text-field
              v-else
              v-model="prime_modifier"
              label="Rate"
              prefix="Prime + "
              suffix="%"
              outlined
              :rules="primeModifierRules"
            />

            <v-text-field
              v-if="!isRevolving"
              v-model="end_date"
              label="End Date"
              type="date"
              outlined
              :rules="endDateRules"
            />
            <v-text-field
              v-if="!isRevolving"
              v-model="minimum_monthly_payment"
              label="Minimum Monthly Payment"
              prefix="$"
              outlined
              :error-messages="minimumMonthlyPaymentErrorMessage"
              :rules="[v => !!v || 'Must provide minimum monthly payment']"
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
import { calculateMinimumAmortizedLoanPayment, asDollar } from '~/assets/utils.js'

export default {
  props: ['visible', 'modalName', 'loanId'],
  data () {
    const loan = this.$store.getters['finances/getLoanById'](this.loanId)
    if (loan) {
      return {
        name: loan.name,
        current_balance: loan.current_balance,
        apr: loan.apr,
        prime_modifier: loan.prime_modifier,
        minimum_monthly_payment: loan.minimum_monthly_payment,
        end_date: loan.end_date,
        id: loan.id,
        interest_type: loan.interest_type,
        loan_type: loan.loan_type
      }
    } else {
      return {
        name: null,
        current_balance: null,
        apr: null,
        minimum_monthly_payment: null,
        end_date: null,
        id: null,
        interest_type: null,
        loan_type: null,
        prime_modifier: null
      }
    }
  },
  computed: {
    // booleans
    showDetails () {
      return this.loan_type !== null & this.interest_type !== null
    },
    isFixed () {
      if (!this.showDetails) {
        return false
      } else {
        return this.interest_type.toUpperCase() === 'FIXED'
      }
    },
    isRevolving () {
      return this.$store.getters['enums/isRevolving'](this.loan_type)
    },

    // enums
    loanTypes () {
      return this.$store.getters['enums/getLoanTypes']
    },
    interestTypes () {
      return this.$store.getters['enums/getInterestTypes']
    },

    // validators
    endDateRules () {
      if (!this.isRevolving) {
        return [v => new Date(v) > new Date() || 'Loans cannot be due in the past']
      } else {
        return []
      }
    },
    minimumMonthlyPaymentErrorMessage () {
      let minPayment = 0
      const interestRate = this.isFixed ? this.apr : 2.5 + Number(this.prime_modifier) // TODO: move current prime to a constants
      if (this.isRevolving) {
        return null
      } else {
        const endDate = new Date(this.end_date)
        if (!this.end_date || endDate <= new Date()) {
          return null
        }
        minPayment = calculateMinimumAmortizedLoanPayment(
          this.current_balance,
          interestRate,
          endDate
        )
      }
      if (minPayment < 10 || this.minimum_monthly_payment >= minPayment) {
        return null
      }
      return `Minimum payment amount must be at least ${asDollar(minPayment)}`
    },
    aprRules () {
      if (this.isRevolving) {
        return [v => !!v || 'Must provide APR']
      } else {
        return []
      }
    },
    primeModifierRules () {
      if (!this.isRevolving) {
        return [v => !!v || 'Must provide prime + rate']
      } else {
        return []
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
      return {
        id: this.id,
        name: this.name,
        current_balance: this.current_balance,
        loan_type: this.loan_type,
        interest_type: this.interest_type,
        minimum_monthly_payment: this.minimum_monthly_payment,
        apr: this.isFixed ? this.apr : null,
        end_date: this.isRevolving ? null : this.end_date,
        prime_modifier: this.isFixed ? null : this.prime_modifier
      }
    }
  }
}
</script>
