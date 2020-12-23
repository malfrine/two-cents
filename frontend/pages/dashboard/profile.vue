<template>
  <ProfileTabs v-if="!isLoading" />
</template>

<script>
import ProfileTabs from '@/components/ProfileTabs.vue'
export default {
  layout: 'dashboard',
  components: {
    ProfileTabs
  },
  computed: {
    isLoading () {
      return this.$store.state.finances.is_loading
    }
  },
  created () {
    // TODO: move isLoading out of store into local data
    if (this.$store.state.finances.no_finances) {
      this.$store.commit('finances/setIsLoading', true)
      this.$store.dispatch('finances/getUserFinances')
    }
  },
  middleware: 'auth'
}
</script>

<style>

</style>
