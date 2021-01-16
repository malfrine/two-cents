<template>
  <div>
    <v-overlay v-if="$fetchState.pending">
      <v-progress-circular
        :size="150"
        color="primary"
        indeterminate
      />
    </v-overlay>
    <template v-else class="stepper">
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
                  <PlanSummary />
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
            <PlanSummary />
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
import { makeFakePlansResponseData, PlanMaker } from '~/assets/plans.js'
import { delay } from '~/assets/utils.js'

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
    await delay(1000) // temp delay to show loading
    const data = makeFakePlansResponseData()
    const pm = new PlanMaker()
    const plans = pm.fromResponseData(data)
    this.$store.commit('plan/SET_PLANS', plans)
  },
  data () {
    return {
      selectedStrategy: 'Two Cents Plan',
      showPanel: false,
      panel: [0, 1, 2, 3]
    }
  },
  computed: {
    netWorthData () {
      console.log("I'm getting the net worth data")
      const refData = this.$store.getters['plan/getNetWorth'](this.selectedStrategy)
      return JSON.parse(JSON.stringify(refData))
    },
    strategies () {
      console.log("I'm getting strategies")
      return this.$store.getters['plan/getStrategies']
    },
    userHasLoans () {
      return (Object.keys(this.loans)).length > 0
    },
    loans () {
      return this.$store.getters['finances/getLoans']
    },
    userHasInvestments () {
      return (Object.keys(this.investments)).length > 0
    },
    investments () {
      return this.$store.getters['finances/getInvestments']
    },
    totalInvestments () {
      let total = 0
      for (const id in this.investments) {
        total += this.investments[id].current_balance
      }
      return total
    },
    totalLoans () {
      let total = 0
      for (const id in this.loans) {
        total += this.loans[id].current_balance
      }
      return total
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
