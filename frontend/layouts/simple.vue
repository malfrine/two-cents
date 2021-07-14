<template>
  <v-app>
    <v-app-bar
      fixed
      :hide-on-scroll="!$vuetify.breakpoint.mobile"
      app
      dark
      flat
      style="background: #121212"
    >
      <div class="d-flex justify-center align-center">
        <NuxtLink to="/">
          <SmallLogo />
        </NuxtLink>
      </div>
    </v-app-bar>
    <v-main>
      <nuxt />
    </v-main>
    <BaseFooter :show-social-links="false" />
  </v-app>
</template>

<script>
import BaseFooter from '@/components/base/BaseFooter'
import SmallLogo from '@/components/logo/SmallLogo.vue'

export default {
  components: {
    BaseFooter,
    SmallLogo
  }
}
</script>
