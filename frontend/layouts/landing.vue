<template>
  <v-app>
    <v-app-bar
      fixed
      :hide-on-scroll="!$vuetify.breakpoint.mobile"
      app
      dark
    >
      <div class="d-flex justify-center align-center">
        <NuxtLink to="/">
          <SmallLogo />
        </NuxtLink>
      </div>
      <v-spacer />
      <v-btn
        outlined
        large
        color="primary"
        href="https://blog.two-cents.ca"
        nuxt
      >
        Blog
      </v-btn>
      <!-- <v-btn
        outlined
        disabled
        large
        color="primary"
        to="/login"
        nuxt
        class="mx-3"
      >
        Login
      </v-btn> -->
    </v-app-bar>
    <v-main>
      <nuxt />
    </v-main>
    <BaseFooter />
  </v-app>
</template>

<script>
import BaseFooter from '@/components/base/BaseFooter.vue'
import SmallLogo from '@/components/logo/SmallLogo.vue'

export default {
  components: {
    BaseFooter,
    SmallLogo
  },
  created () {
    this.$vuetify.theme.isDark = false
  }
}
</script>
