<template>
  <BaseLoadingResultComponent
    :loading="!planExists"
    error=""
    :success="planExists"
  >
    <template v-slot:success>
      <ProfileTabs :published-plan-id="publishedPlanId" />
    </template>
  </BaseLoadingResultComponent>
</template>

<script>
import BaseLoadingResultComponent from '@/components/base/BaseLoadingResultComponent.vue'
import ProfileTabs from '@/components/dashboard/ProfileTabs.vue'

export default {
  layout: 'published-plan',
  components: {
    BaseLoadingResultComponent,
    ProfileTabs
  },
  fetch () {
    this.$store.dispatch('published-plans/getPlanIfNotExists', { id: this.publishedPlanId })
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
