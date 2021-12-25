<template>
  <BaseLoadingResultComponent
    :loading="!planExists"
    error=""
    :success="planExists"
  >
    <template v-slot:success>
      <FullFinancialPlan
        :is-paid-user="true"
        :is-admin-user="isAdminUser"
        :published-plan-id="publishedPlanId"
        @show-upgrade-dialog="showPlanUpgradeDialog=true"
      />
    </template>
  </BaseLoadingResultComponent>
</template>

<script>
import BaseLoadingResultComponent from '@/components/base/BaseLoadingResultComponent.vue'
import FullFinancialPlan from '@/components/plan/FullFinancialPlan.vue'

export default {
  layout: 'published-plan',
  components: {
    FullFinancialPlan,
    BaseLoadingResultComponent
  },
  fetch () {
    this.$store.dispatch('enums/getAllEnumsIfNeeded')
    this.$store.dispatch('published-plans/getPlanIfNotExists', { id: this.publishedPlanId })
  },
  data () {
    return {
      isPaidUser: true, // HACK: to make the FullFinancialPlan show everything
      isAdminUser: false // HACK: to make the FullFinancialPlan show everything
    }
  },
  computed: {
    publishedPlanId () {
      return Number(this.$route.params.id)
    },
    planExists () {
      return this.$store.getters['published-plans/getPublishedPlanExists'](this.publishedPlanId)
    }
  },
  beforeMount () {
    this.$fetch()
  },
  head () {
    return {
      title: 'Financial Plan'
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
