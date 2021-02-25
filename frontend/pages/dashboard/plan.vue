<template>
  <div>
    <v-overlay v-if="userFinancesValidationError" absolute opacity="0">
      <v-alert
        prominent
        type="error"
        style="max-width: 600px"
      >
        {{ userFinancesValidationError }}
      </v-alert>
    </v-overlay>
    <v-overlay v-else-if="$fetchState.pending" absolute opacity="0">
      <v-progress-circular
        :size="150"
        color="primary"
        indeterminate
      />
    </v-overlay>
    <v-overlay v-else-if="!planExists" absolute opacity="0">
      <v-alert
        prominent
        type="error"
        style="max-width: 600px"
      >
        Sorry, there was an error building your plan. We are working on fixing the problem.
      </v-alert>
    </v-overlay>
    <template v-else>
      <v-card>
        <v-container fluid>
          <v-row align="center" align-content="center" justify="center" justify-md="space-between">
            <v-col cols="12" md="8" class="d-flex align-center justify-center justify-md-start">
              <div class="text-h4 text-sm-h3 text-md-h2 text-center text-md-start">
                {{ possessiveUserName }} Financial Plan
              </div>
            </v-col>
            <v-col v-if="!$vuetify.breakpoint.mdAndUp" cols="12" sm="8" md="4">
              <v-select
                v-model="selectedStrategy"
                label="Pick a Financial Plan"
                solo
                outlined
                item-color="primary"
                :items="strategies"
                class="mb-n7"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-card>
      <v-row>
        <v-col cols="12" md="8" lg="9" class="mr-n3">
          <v-expansion-panels
            v-model="panel"
            multiple
          >
            <v-container v-if="!$vuetify.breakpoint.mdAndUp" fluid>
              <v-expansion-panel class="my-n1">
                <v-expansion-panel-header>
                  <div class="text-h5">
                    Summary
                  </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <PlanSummary :selected-strategy="selectedStrategy" />
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-container>
            <v-container fluid>
              <v-expansion-panel class="my-n1">
                <v-expansion-panel-header>
                  <div class="text-h5">
                    Net Worth Projection
                  </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-card>
                    <v-container>
                      <NetWorthChart :chart-data="netWorthData" :style="chartStyles" />
                    </v-container>
                  </v-card>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-container>
            <v-container fluid>
              <v-expansion-panel class="my-n1">
                <v-expansion-panel-header>
                  <div class="text-h5">
                    Current Finances
                  </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <PlanCurrentFinances />
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-container>
            <v-container fluid>
              <v-expansion-panel class="my-n1">
                <v-expansion-panel-header>
                  <div class="text-h5">
                    Milestones
                  </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content style="max-height: 600px" class="overflow-y-auto">
                  <v-card>
                    <v-container>
                      <PlanMilestones :selected-strategy="selectedStrategy" />
                    </v-container>
                  </v-card>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-container>
            <v-container fluid>
              <v-expansion-panel class="my-n1">
                <v-expansion-panel-header>
                  <div class="text-h5">
                    Action Plan
                  </div>
                </v-expansion-panel-header>
                <v-expansion-panel-content style="max-height: 600px" class="overflow-y-auto">
                  <v-container>
                    <PlanActionPlan :selected-strategy="selectedStrategy" />
                  </v-container>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-container>
          </v-expansion-panels>
        </v-col>
        <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="3" md="4" lg="3">
          <v-card
            max-width="344"
            class="sticky-nav mt-2"
          >
            <v-container>
              <v-select
                v-model="selectedStrategy"
                label="Pick a Financial Plan"
                solo
                outlined
                item-color="primary"
                :items="strategies"
                class="mb-n7"
              />
            </v-container>
            <v-divider class="my-2" />
            <PlanSummary :selected-strategy="selectedStrategy" />
          </v-card>
        </v-col>
      </v-row>
    </template>
  </div>
</template>

<script>
import NetWorthChart from '@/components/plan/net-worth-chart.js'
import PlanMilestones from '@/components/plan/PlanMilestones.vue'
import PlanCurrentFinances from '@/components/plan/PlanCurrentFinances.vue'
import PlanSummary from '@/components/plan/PlanSummary.vue'
import { PlanMaker } from '~/assets/plans.js'
import { asDollar } from '~/assets/utils.js'

export default {
  layout: 'dashboard',
  middleware: 'auth',
  components: {
    NetWorthChart,
    PlanMilestones,
    PlanCurrentFinances,
    PlanSummary
  },
  async fetch () {
    if (this.userFinancesValidationError) {
      return null
    }
    const financesUpdated = this.$store.getters['finances/getFinancesUpdateSinceLastPlanBuilt']
    if (this.planExists & !financesUpdated) {
      console.log('A plan exists and the finances were not updated - not getting a new plan')
      return null
    }
    this.$store.commit('plan/RESET_PLANS')
    const response = await this.$axios.$get('/api/my/plan')
      .then((response) => {
        return response
      })
      .catch((e) => {
        // this.$toast.error('Could not get your plan')
        return null
      })
    console.log(this.$store.getters['plan/getIsPlansAvailable'])
    if (response) {
      const pm = new PlanMaker()
      const plans = pm.fromResponseData(response)
      this.$store.commit('plan/SET_PLANS', plans)
      this.$store.commit('finances/REGISTER_PLAN_UPDATED')
    }
  },
  data () {
    return {
      selectedStrategy: 'Two Cents Plan',
      panel: [0, 1, 2, 3]
    }
  },
  computed: {
    planExists () {
      return this.$store.getters['plan/getIsPlansAvailable']
    },
    netWorthData () {
      const refData = this.$store.getters['plan/getNetWorth'](this.selectedStrategy)
      return JSON.parse(JSON.stringify(refData))
    },
    strategies () {
      return this.$store.getters['plan/getStrategies']
    },
    possessiveUserName () {
      const firstName = this.$store.getters['finances/getFirstName']
      const posession = firstName.slice(-1) === 's' ? "'" : "'s"
      return `${firstName}${posession}`
    },
    chartHeight () {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 300
        case 'sm': return 400
        case 'md': return 400
        case 'lg': return 600
        case 'xl': return 700
      }
      return 800
    },
    chartStyles () {
      return {
        position: 'relative',
        height: `${this.chartHeight}px`
      }
    },
    userFinancesValidationError () {
      const financialProfile = this.$store.getters['finances/getFinancialProfile']
      if (Object.keys(financialProfile).length === 0) {
        return 'Please add a monthly allowance and retirement age.'
      }

      const loans = this.$store.getters['finances/getLoans']
      const investments = this.$store.getters['finances/getInvestments']
      if (Object.keys(loans).length === 0 && Object.keys(investments).length === 0) {
        return 'Please add at least one loan or investment.'
      }

      let totalMinimumMonthlyPayments = 0
      for (const loanId in loans) {
        console.log(loans[loanId].minimum_monthly_payment || 0)
        totalMinimumMonthlyPayments += loans[loanId].minimum_monthly_payment || 0
      }
      for (const investmentId in investments) {
        console.log(investments[investmentId].pre_authorized_monthly_contribution || 0)
        totalMinimumMonthlyPayments += investments[investmentId].pre_authorized_monthly_contribution || 0
      }
      console.log(totalMinimumMonthlyPayments)
      console.log(financialProfile.monthly_allowance)
      if (totalMinimumMonthlyPayments > financialProfile.monthly_allowance) {
        return `Your plan cannot be created because your monthly allowance (${asDollar(financialProfile.monthly_allowance)}) 
                is less than the required minimum monthly payment (${asDollar(totalMinimumMonthlyPayments)}). Please increase your monthly allowance.`
      }

      return ''
    }
  },
  head () {
    return {
      title: 'Plan'
    }
  }
}
</script>

<style scoped>
.sticky-nav {
  position: -webkit-sticky;
  position: sticky;
  top: 4.5rem;
}
</style>
