<template>
  <ProfileTabs v-if="!isLoading" />
</template>

<script>
import ProfileTabs from '@/components/dashboard/ProfileTabs.vue'
export default {
  components: {
    ProfileTabs
  },
  computed: {
    isLoading () {
      return this.$store.state.finances.is_loading
    }
  },
  mounted () {
    // TODO: move isLoading out of store into local data
    if (this.$store.state.finances.no_finances) {
      this.$store.commit('finances/setIsLoading', true)
      this.$store.dispatch('finances/getUserFinances')
    }
  },
  head () {
    return {
      title: 'Profile'
    }
  },
  layout: 'dashboard',
  middleware: 'auth'
}
</script>

<style>

</style>
