<template>
  <BaseExpandableObjectCard
    :name="loan.name"
    :summary-value="summaryValue"
    :summary-color="$instrument.colors.getColor('loan', loanId)"
    :icon="$instrument.icons.getIcon(loanType)"
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
        <p v-if="isMortgage" class="mt-n3">
          <em> Current Term End Date: </em> {{ loanInterest.current_term_end_date }}
        </p>
        <p v-for="(object, fieldName) in mortgageFields" :key="fieldName" class="mt-n3">
          <em>{{ object.labelName }}:</em> {{ getDetailString(fieldName, object) }}
        </p>
        <p v-for="(object, fieldName) in instalmentLoanFields" v-show="isInstalmentLoan" :key="fieldName" class="mt-n3">
          <em>{{ object.labelName }}:</em> {{ getDetailString(fieldName, object) }}
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
  props: { loanId: { type: Number, required: true } },
  data () {
    const mortgageFields = {
      minimum_monthly_payment: {
        labelName: 'Monthly Payment',
        type: 'dollar'
      },
      end_date: {
        labelName: 'Mortgage End Date',
        type: 'date'
      }
    }

    const instalmentLoanFields = {
      minimum_monthly_payment: {
        labelName: 'Minimum Monthly Payment',
        type: 'dollar'
      },
      end_date: {
        labelName: 'Loan End Date',
        type: 'date'
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
      return asDollar(this.loan.current_balance)
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
    getDetailString (fieldName, fieldObject) {
      const value = this.loan[fieldName]
      const valueStr = fieldObject.type === 'dollar' && value ? asDollar(value) : String(value)
      const suffix = fieldObject.suffix || ''
      return `${valueStr}${suffix}`
    }

  }
}
</script>
