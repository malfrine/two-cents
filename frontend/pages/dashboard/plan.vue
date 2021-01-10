<template>
  <div>
    <v-overlay v-if="isLoading">
      <v-progress-circular
        :size="150"
        color="primary"
        indeterminate
      />
    </v-overlay>
    <template v-else>
      <v-card>
        <v-container fluid>
          <v-row align="center" align-content="center" justify="center" justify-md="space-between">
            <v-col cols="12" md="8" class="d-flex align-center justify-center justify-md-start">
              <div class="text-h4 text-sm-h3 text-md-h2 text-center text-md-start">
                {{ planName }}
              </div>
            </v-col>
            <v-col cols="6" md="4">
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

      <v-container>
        <v-card>
          <v-container ref="chart">
            <NetWorthChart :chart-data="netWorthData" :style="chartStyles" />
          </v-container>
        </v-card>
      </v-container>
    </template>
  </div>
</template>

<script>
import NetWorthChart from '@/components/plan/net-worth-chart.js'
import { makeFakePlan, RawPlanProcessor } from '~/assets/plan-utils.js'
import { delay } from '~/assets/utils.js'

export default {
  layout: 'dashboard',
  middleware: 'auth',
  components: {
    NetWorthChart
  },
  async fetch () {
    this.isLoading = true
    await delay(1000) // temp delay to show loading
    const data = await makeFakePlan()
    const rp = new RawPlanProcessor()
    rp.processResponse(data)
    this.$store.commit('plan/SET_PLAN', data)
    this.isLoading = false
  },
  data () {
    return {
      isLoading: false,
      selectedStrategy: 'Two Cents Plan'

    }
  },
  computed: {
    planData () {
      return {
        netWorth: this.$store.getters['plan/getNetWorth'],
        summary: this.$store.getters['plan/getSummary'],
        strategies: this.$store.getters['plan/getStrategies']
      }
    },
    netWorthData () {
      return JSON.parse(JSON.stringify(this.planData.netWorth[this.selectedStrategy]))
    },
    strategies () {
      return this.planData.strategies
    },
    planSummary () {
      return this.planData.summary
    },
    planName () {
      const firstName = this.$store.getters['finances/getFirstName']
      return `${firstName}'s Financial Plan`
    },
    chartHeight () {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 300
        case 'sm': return 400
        case 'md': return 500
        case 'lg': return 500
        case 'xl': return 600
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
