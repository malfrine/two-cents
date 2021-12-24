<template>
  <div>
    <v-overlay z-index="2" :value="userFinancesValidationError" absolute opacity="0">
      <v-alert
        prominent
        type="error"
        style="max-width: 600px"
      >
        {{ userFinancesValidationError }}
      </v-alert>
    </v-overlay>
    <v-overlay z-index="2" :value="$fetchState.pending" opacity="0">
      <v-progress-circular
        :size="150"
        color="primary"
        indeterminate
      />
    </v-overlay>
    <v-overlay z-index="2" :value="errorBuildingPlan" opacity="0">
      <v-alert
        prominent
        type="error"
        style="max-width: 600px"
      >
        Sorry, there was an error building your plan. We are working on fixing the problem.
      </v-alert>
    </v-overlay>
    <PlanUpgradeDialog
      :visible="showPlanUpgradeDialog"
      @close="showPlanUpgradeDialog=false"
      @payment-made="showPlanUpgradeDialog=false"
    />
    <template v-if="receivedValidPlanData">
      <FullFinancialPlan
        :is-paid-user="isPaidUser"
        :is-admin-user="isAdminUser"
        @show-upgrade-dialog="showPlanUpgradeDialog=true"
      />
    </template>
  </div>
</template>

<script>
import FullFinancialPlan from '@/components/plan/FullFinancialPlan.vue'
import PlanUpgradeDialog from '@/components/plan/PlanUpgradeDialog.vue'
import { PlanMaker } from '~/assets/plans.js'

export default {
  layout: 'dashboard',
  middleware: 'auth',
  components: {
    FullFinancialPlan,
    PlanUpgradeDialog
  },
  async fetch () {
    this.$fire.analytics.logEvent('plan_creation_attempt')
    if (this.userFinancesValidationError) {
      return null
    }
    const financesUpdated = this.$store.getters['finances/getFinancesUpdateSinceLastPlanBuilt']
    if (this.planExists & !financesUpdated) {
      return null
    }
    this.$store.commit('plan/RESET_PLANS')
    const response = await this.$axios.$get('/api/my/plan')
      .then((response) => {
        return response
      })
      .catch((e) => {
        // exception is logged server side
        return null
      })
    if (response) {
      const pm = new PlanMaker(this.$instrument.colors)
      const plans = pm.fromResponseData(response)
      this.$store.commit('plan/SET_PLANS', plans)
      this.$store.commit('finances/REGISTER_PLAN_UPDATED')
      this.$fire.analytics.logEvent('created_plan')
    }
  },
  data () {
    return {
      showPlanUpgradeDialog: false
    }
  },
  computed: {
    userFinancesValidationError () {
      const loans = this.$store.getters['finances/getLoans']
      const investments = this.$store.getters['finances/getInvestments']
      if (Object.keys(loans).length === 0 && Object.keys(investments).length === 0) {
        return 'Please add at least one loan or investment.'
      }
      return ''
    },
    isPaidUser () {
      return this.$store.getters['users/getShowFullPlan'] || this.isAdminUser
    },
    isAdminUser () {
      return this.$store.getters['users/getIsAdminUser']
    },
    errorBuildingPlan () {
      return !this.userFinancesValidationError && !this.$fetchState.pending && !this.planExists
    },
    receivedValidPlanData () {
      if (this.userFinancesValidationError) {
        return false
      }
      if (this.$fetchState.pending) {
        return false
      }
      if (this.errorBuildingPlan) {
        return false
      }
      return true
    },
    planExists () {
      return this.$store.getters['plan/getIsPlansAvailable']
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
