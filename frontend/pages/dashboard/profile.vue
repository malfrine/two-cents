<template>
  <v-container>
    <v-overlay v-if="isLoading">
      <v-progress-circular
        :size="150"
        color="primary"
        indeterminate
      />
    </v-overlay>
    <ProfileTabs v-else />
  </v-container>
</template>

<script>
import ProfileTabs from '@/components/dashboard/ProfileTabs.vue'
export default {
  components: {
    ProfileTabs
  },
  async fetch () {
    if (!this.$store.getters['finances/getUserFinancesExists']) {
      this.isLoading = true
      const response = await this.$axios.$get('/api/my/finances')
        .then((response) => {
          return response
        })
        .catch((e) => {
          this.$sentry.captureException('Unable to get users financial information', e)
          this.$toast.error('Could not get your financial information')
          // todo show an error modal
          this.isLoading = false
          return null
        })
      this.$store.commit('finances/SET_USER_FINANCES', response.financial_data)
      this.$store.commit('users/SET_USER_INFO', response)
      this.isLoading = false
    }
  },
  data () {
    return {
      isLoading: false
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
