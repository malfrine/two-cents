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
      console.log('no user finances available - going to fetch it')
      this.isLoading = true
      const response = await this.$axios.$get('/api/my/finances')
        .then((response) => {
          if (response.financial_profile == null) {
            response.financial_profile = {}
          // TODO: do this in a cleaner way
          }
          return response
        })
        .catch((e) => {
          this.$toast.error('Could not get your financial information')
          return null
        })
      this.$store.commit('finances/SET_USER_FINANCES', response)
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
