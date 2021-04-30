<template>
  <v-app>
    <v-app-bar
      fixed
      app
      dark
      min-height="78"
      class="pt-2"
    >
      <div class="d-flex justify-center">
        <NuxtLink to="/">
          <SmallLogo />
        </NuxtLink>
      </div>
      <v-spacer />
      <v-btn icon @click.prevent="$vuetify.theme.isDark = !$vuetify.theme.isDark">
        <v-icon>mdi-theme-light-dark</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <nuxt />
      </v-container>
    </v-main>
    <BaseFooter />
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
