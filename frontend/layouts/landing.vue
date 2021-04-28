<template>
  <v-app>
    <v-app-bar
      fixed
      hide-on-scroll
      app
      dark
    >
      <div class="d-flex justify-center align-center">
        <v-img
          max-width="120"
          max-height="50"
          src="/logo-white.png"
        />
      </div>
      <v-spacer />
      <v-btn outlined large color="primary" to="/login" nuxt>
        Login
      </v-btn>
    </v-app-bar>
    <v-main>
      <nuxt />
    </v-main>
    <LandingFooter />
  </v-app>
</template>

<script>
import LandingFooter from '@/components/landing/LandingFooter.vue'

export default {
  components: {
    LandingFooter
  },
  created () {
    this.$vuetify.theme.isDark = false
  }
}
</script>
