<template>
    <dashboard-layout>
      <ProfileTabs v-if="!isLoading" />
  </dashboard-layout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'
import ProfileTabs from '@/components/ProfileTabs.vue'
export default {
  components: {
    DashboardLayout,
    ProfileTabs
  },
  created: function() {
    // TODO: move isLoading out of store into local data
    this.$store.commit('finances/setIsLoading', true)
    this.$store.dispatch('finances/getUserFinances')
  },
  computed: {
    isLoading() {
      return this.$store.state["finances"]["is_loading"]
    }
  }
}
</script>

<style>

</style>
