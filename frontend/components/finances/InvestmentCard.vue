<template>
  <base-instrument-card>
    <template v-slot:fixed>
      <v-row class="mx-3">
        <v-card-subtitle class="mb-n7">
          <div class="text-h6">
            {{ investment.name }}
          </div>
        </v-card-subtitle>
        <v-spacer />
        <v-speed-dial
          v-model="fab"
          direction="bottom"
          class="mt-2"
        >
          <template v-slot:activator>
            <v-btn
              v-model="fab"
              icon
              fab
              small
            >
              <v-icon v-if="fab">
                mdi-close
              </v-icon>
              <v-icon v-else>
                mdi-dots-horizontal
              </v-icon>
            </v-btn>
          </template>
          <v-btn
            fab
            small
            color="blue"
            @click.stop="showInvestmentDialog=true"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            fab
            small
            color="red"
            @click.prevent="deleteInvestment(investment)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-speed-dial>

        <InvestmentDialog :visible="showInvestmentDialog" :investment-id="investment.id" @close="showInvestmentDialog=false" />
      </v-row>
      <v-card-title>
        <div v-if="!isGuaranteedInvestment" class="text-h2 primary--text" color="primary">
          {{ asDollar(investment.current_balance) }}
        </div>
        <div v-else class="text-h2 primary--text" color="primary">
          {{ asDollar(investment.principal_investment_amount) }}
        </div>
      </v-card-title>
    </template>
    <template v-slot:hidden>
      <v-card-text>
        <p class="mt-n5">
          <em>Investment Type:</em> {{ investment.investment_type }}
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
        <p v-if="requiredFields.includes('volatility_choice')" class="mt-n3">
          <em>Volatility:</em> {{ investment.volatility_choice }}
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
  </base-instrument-card>
</template>

<script>
import { mapActions } from 'vuex'
import InvestmentDialog from '@/components/finances/InvestmentDialog.vue'
import { asDollar } from '~/assets/utils.js'

export default {
  components: {
    InvestmentDialog
  },
  props: ['investmentId'],
  data () {
    return {
      showInvestmentDialog: false,
      showAllInfo: false,
      fab: false
    }
  },
  methods: {
    ...mapActions('finances', ['deleteInvestment']), asDollar
  },
  computed: {
    investment () {
      return this.$store.getters['finances/getInvestmentById'](this.investmentId)
    },
    requiredFields () {
      return this.$store.getters['enums/getRequiredFields'](this.investment.investment_type)
    },
    isVariable () {
      const interestType = this.investment.interest_type
      return interestType && interestType.toUpperCase() === 'VARIABLE'
    },
    isGuaranteedInvestment () {
      console.log(this.requiredFields.includes('principal_investment_amount'))
      return this.requiredFields.includes('principal_investment_amount')
    }
  }
}
</script>
