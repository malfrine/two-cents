<template>
  <v-app>
    <v-app-bar
      fixed
      app
      dark
    >
      <div class="d-flex justify-center">
        <v-img
          max-width="150"
          max-height="65"
          src="/logo-white.png"
        />
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

export default {
  components: {
    BaseFooter
  }
}
</script>
