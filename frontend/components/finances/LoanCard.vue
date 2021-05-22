<template>
  <BaseExpandableObjectCard
    :name="loan.name"
    :summary-value="summaryValue"
    @open-dialog="showLoanDialog = true"
    @delete-object="deleteLoan(loan)"
  >
    <template v-slot:dialog>
      <LoanDialog :visible="showLoanDialog" :loan-id="loan.id" @close="showLoanDialog=false" />
    </template>
    <template v-slot:hidden>
      <v-card-text>
        <p class="mt-n3">
          <em> Loan Type: </em> {{ loanType }}
        </p>
        <p class="mt-n3">
          <em> Interest Rate: </em> {{ interestRateValue }}
        </p>
        <p v-for="(object, fieldName) in mortgageFields" v-show="isMortgage" :key="fieldName" class="mt-n3">
          <em>{{ object.labelName }}:</em> {{ getDetailString(mortgageDetails, fieldName, object) }}
        </p>
        <p v-for="(object, fieldName) in instalmentLoanFields" v-show="isInstalmentLoan" :key="fieldName" class="mt-n3">
          <em>{{ object.labelName }}:</em> {{ getDetailString(loan, fieldName, object) }}
        </p>
      </v-card-text>
    </template>
  </BaseExpandableObjectCard>
</template>

<script>
import { mapActions } from 'vuex'
import LoanDialog from '@/components/finances/LoanDialog.vue'
import LoanDetailsMixin from '@/mixins/LoanDetailsMixin.js'
import { asDollar } from '~/assets/utils.js'

export default {
  components: {
    LoanDialog
  },
  mixins: [LoanDetailsMixin],
  props: { loanId: Number },
  data () {
    const mortgageFields = {
      monthly_payment: {
        labelName: 'Monthly Mortgage Payment',
        type: 'dollar'
      },
      downpayment_amount: {
        labelName: 'Downpayment',
        type: 'dollar'
      },
      purchase_date: {
        labelName: 'Purchase Date',
        type: 'dollar'
      },
      amortization_years: {
        labelName: 'Mortgage Length',
        suffix: ' years'
      },
      current_term_start_date: {
        labelName: 'Current Term Start Date'
      },
      current_term_years: {
        labelName: 'Current Term Length',
        suffix: ' years'
      }
    }

    const instalmentLoanFields = {
      minimum_monthly_payment: {
        labelName: 'Minimum Monthly Payment',
        type: 'dollar'
      }
    }

    return {
      instalmentLoanFields,
      mortgageFields,
      instalmentLoans: ['Personal Loan', 'Student Loan', 'Car Loan'],
      revolvingLoans: ['Line of Credit', 'Credit Card', 'Student Line of Credit'],
      mortgageTypeLabel: 'Mortgage',
      fixedInterestRateLabel: 'Fixed',
      showLoanDialog: false,
      showAllInfo: false,
      fab: false
    }
  },
  computed: {
    summaryValue () {
      return this.isMortgage ? asDollar(this.mortgageDetails.purchase_price) : asDollar(this.loan.current_balance)
    },
    interestRateValue () {
      let rateStr = ''
      if (this.isFixedInterestRate) {
        rateStr = `${this.loanInterest.apr}% APR`
      } else if (this.isVariableInterestRate) {
        rateStr = `Prime Rate + ${this.loanInterest.prime_modifier}%`
      }
      const mortgageSuffix = this.isMortgage ? '(Current Term)' : ''
      return `${rateStr} ${mortgageSuffix}`
    },
    loan () {
      return this.$store.getters['finances/getLoanById'](this.loanId) || {}
    },
    loanInterest () {
      return this.loan.loan_interest || {}
    },
    mortgageDetails () {
      return this.isMortgage ? this.loan.mortgage_details || {} : {}
    },
    loanType () {
      return this.loan.loan_type
    },
    interestType () {
      return this.loanInterest.interest_type
    }
  },
  methods: {
    ...mapActions('finances', ['deleteLoan']),
    asDollar,
    getDetailString (dataObject, fieldName, fieldObject) {
      const value = dataObject[fieldName]
      const valueStr = fieldObject.type === 'dollar' && value ? asDollar(value) : String(value)
      const suffix = fieldObject.suffix || ''
      return `${valueStr}${suffix}`
    }

  }
}
</script>
