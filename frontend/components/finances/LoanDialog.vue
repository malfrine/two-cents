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
            v-model="name"
            label="Loan Name"
            outlined
          />
          <v-text-field
            v-model="current_balance"
            label="Current Balance"
            prefix="$"
            outlined
          />
          <v-text-field
            v-model="apr"
            label="APR"
            suffix="%"
            outlined
          />
          <v-text-field
            v-model="end_date"
            label="End Date"
            type="date"
            outlined
            :rules="endDateRules"
          />
          <v-text-field
            v-model="minimum_monthly_payment"
            label="Minimum Monthly Payment"
            prefix="$"
            outlined
            :error-messages="minimumMonthlyPaymentErrorMessage"
          />
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
    const endDateRules = [v => new Date(v) > new Date() || 'Loans cannot be due in the past']
    if (loan) {
      return {
        name: loan.name,
        current_balance: loan.current_balance,
        apr: loan.apr,
        minimum_monthly_payment: loan.minimum_monthly_payment,
        end_date: loan.end_date,
        id: loan.id,
        endDateRules
      }
    } else {
      return {
        name: null,
        current_balance: null,
        apr: null,
        minimum_monthly_payment: null,
        end_date: null,
        id: null,
        endDateRules
      }
    }
  },
  computed: {
    minimumMonthlyPaymentErrorMessage () {
      if (!this.end_date || this.end_date <= new Date()) {
        return null
      }
      const minPayment = calculateMinimumAmortizedLoanPayment(
        this.current_balance,
        this.apr,
        new Date(this.end_date)
      )
      if (minPayment < 10 || this.minimum_monthly_payment >= minPayment) {
        return null
      }
      return `Minimum payment amount must be at least ${asDollar(minPayment)}`
    },
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
      const isValid = this.$refs.form.validate()
      if (!isValid || this.minimumMonthlyPaymentErrorMessage) {
        return // don't submit if does not pass validation or contain error
      }
      this.show = false
      this.$store.dispatch('finances/createOrUpdateLoan', {
        name: this.name,
        current_balance: this.current_balance,
        apr: this.apr,
        minimum_monthly_payment: this.minimum_monthly_payment,
        end_date: this.end_date,
        id: this.id
      })
    }
  }
}
</script>
