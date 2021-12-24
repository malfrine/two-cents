<template>
  <BaseExpandableObjectCard
    :name="investment.name"
    :summary-value="summaryValue"
    :summary-color="$instrument.colors.getColor('investment', investmentId)"
    :icon="$instrument.icons.getIcon(investment.investment_type)"
    :read-only="readOnly"
    @open-dialog="showInvestmentDialog = true"
    @delete-object="deleteInvestment(investment)"
  >
    <template v-slot:dialog>
      <InvestmentDialog :visible="showInvestmentDialog" :investment-id="investment.id" @close="showInvestmentDialog=false" />
    </template>
    <template v-slot:hidden>
      <v-card-text>
        <p class="mt-n5">
          <em>Investment Type:</em> {{ investment.investment_type }}
        </p>
        <p class="mt-n3">
          <em>Account Type:</em> {{ investment.account_type }}
        </p>
        <p v-if="requiredFields.includes('risk_level')" class="mt-n3">
          <em>Risk Level:</em> {{ investment.risk_level }}
        </p>
        <p v-if="requiredFields.includes('pre_authorized_monthly_contribution')" class="mt-n3">
          <em>Pre-Authorized Monthly Contribution:</em> {{ asDollar(investment.pre_authorized_monthly_contribution) }}
        </p>
        <p v-if="requiredFields.includes('expected_roi') && !isVariable" class="mt-n3">
          <em>Expected Return on Investment:</em> {{ investment.expected_roi }}%
        </p>
        <p v-else-if="isVariable" class="mt-n3">
          <em>Prime + </em> {{ investment.prime_modifier }}%
        </p>
        <p v-if="requiredFields.includes('symbol')" class="mt-n3">
          <em>Ticker Symbol:</em> {{ investment.symbol }}
        </p>
        <p v-if="requiredFields.includes('principal_investment_amount')" class="mt-n3">
          <em>Principal Investment:</em> {{ asDollar(investment.principal_investment_amount) }}
        </p>
        <p v-if="requiredFields.includes('volatility_choice')" class="mt-n3">
          <em>Volatility:</em> {{ investment.volatility_choice }}
        </p>
        <p v-if="requiredFields.includes('investment_date')" class="mt-n3">
          <em>Investment Date:</em> {{ investment.investment_date }}
        </p>
        <p v-if="requiredFields.includes('maturity_date')" class="mt-n3">
          <em>Maturity Date:</em> {{ investment.maturity_date }}
        </p>
      </v-card-text>
    </template>
  </BaseExpandableObjectCard>
</template>

<script>
import { mapActions } from 'vuex'
import InvestmentDialog from '@/components/finances/InvestmentDialog.vue'
import { asDollar } from '~/assets/utils.js'

export default {
  components: {
    InvestmentDialog
  },
  props: {
    investmentId: {
      type: Number,
      required: true
    },
    readOnly: {
      type: Boolean,
      default: false
    },
    publishedPlanId: {
      type: Number,
      default: null
    }
  },
  data () {
    return {
      showInvestmentDialog: false,
      showAllInfo: false,
      fab: false
    }
  },
  computed: {
    investment () {
      if (this.publishedPlanId != null) {
        return this.$store.getters['published-plans/getInvestmentById'](this.publishedPlanId, this.investmentId) || {}
      } else {
        return this.$store.getters['finances/getInvestmentById'](this.investmentId)
      }
    },
    requiredFields () {
      return this.$store.getters['enums/getRequiredFields'](this.investment.investment_type)
    },
    isVariable () {
      const interestType = this.investment.interest_type
      return interestType && interestType.toUpperCase() === 'VARIABLE'
    },
    isGuaranteedInvestment () {
      return this.requiredFields.includes('principal_investment_amount')
    },
    summaryValue () {
      return this.isGuaranteedInvestment ? asDollar(this.investment.principal_investment_amount) : asDollar(this.investment.current_balance)
    }
  },
  methods: {
    ...mapActions('finances', ['deleteInvestment']), asDollar
  }
}
</script>
