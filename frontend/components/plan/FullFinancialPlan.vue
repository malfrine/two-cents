<template>
  <div>
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
    <v-row justify="center">
      <v-col cols="12" md="8" lg="9">
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
          <v-container fluid @click="handlePremiumFeatureInterest">
            <v-expansion-panel class="my-n1" :disabled="!isPaidUser">
              <v-expansion-panel-header>
                <v-card-title class="text-h5">
                  Net Worth Projection <TooltipIcon :text="tooltips.netWorthProjection" />
                </v-card-title>
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
          <v-container fluid @click="handlePremiumFeatureInterest">
            <v-expansion-panel class="my-n1" :disabled="!isPaidUser">
              <v-expansion-panel-header>
                <v-card-title class="text-h5">
                  Current Finances <TooltipIcon :text="tooltips.currentFinances" />
                </v-card-title>
              </v-expansion-panel-header>
              <v-expansion-panel-content>
                <PlanCurrentFinances />
              </v-expansion-panel-content>
            </v-expansion-panel>
          </v-container>

          <v-container fluid>
            <v-expansion-panel class="my-n1">
              <v-expansion-panel-header>
                <v-card-title class="text-h5">
                  Milestones <TooltipIcon :text="tooltips.milestones" />
                </v-card-title>
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
                <v-card-title class="text-h5">
                  Action Plan <TooltipIcon :text="tooltips.actionPlan" />
                </v-card-title>
              </v-expansion-panel-header>
              <v-expansion-panel-content style="max-height: 600px" class="overflow-y-auto">
                <v-container>
                  <PlanActionPlan
                    :selected-strategy="selectedStrategy"
                    :is-premium-plan="isPaidUser"
                    @show-upgrade-dialog="handlePremiumFeatureInterest"
                  />
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
            <TCTooltip :text="tooltips.strategies" left>
              <template v-slot:inner>
                <v-select
                  v-model="selectedStrategy"
                  label="Pick a Financial Plan"
                  solo
                  outlined
                  item-color="primary"
                  :items="strategies"
                  class="mb-n7"
                />
              </template>
            </TCTooltip>
            <v-btn
              v-if="!isPaidUser"
              class="gradient mt-3"
              block
              large
              @click="handlePremiumFeatureInterest"
            >
              See full plan
            </v-btn>
          </v-container>
          <v-divider class="my-2" />
          <PlanSummary :selected-strategy="selectedStrategy" />
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import NetWorthChart from '@/components/plan/net-worth-chart.js'
import PlanMilestones from '@/components/plan/PlanMilestones.vue'
import PlanCurrentFinances from '@/components/plan/PlanCurrentFinances.vue'
import PlanSummary from '@/components/plan/PlanSummary.vue'
import TooltipIcon from '@/components/base/TooltipIcon.vue'
import TCTooltip from '@/components/base/TCTooltip.vue'
import PlanDataMixin from '@/mixins/PlanDataMixin.js'

export default {
  components: {
    NetWorthChart,
    PlanMilestones,
    PlanCurrentFinances,
    PlanSummary,
    TooltipIcon,
    TCTooltip
  },
  mixins: [PlanDataMixin],
  props: {
    isPaidUser: {
      default: false,
      type: Boolean
    }
  },
  data () {
    return {
      panel: this.isPaidUser ? [0] : [2],
      showPlanUpgradeDialog: false
    }
  },
  methods: {
    handlePremiumFeatureInterest () {
      if (!this.isPaidUser) {
        this.$emit('show-upgrade-dialog')
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

.gradient {
background: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%) 1 stretch;
}

.gradient-border {
border-color: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%) 1 stretch;
}
</style>
