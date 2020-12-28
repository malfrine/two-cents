<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" lg="5" md="7">
        <v-card>
          <v-img
            src="/big-logo-dark.png"
          />
          <div class="text-subtitle1 text-center">
            DIY financial planning powered by AI
          </div>
          <v-divider class="my-5" />
          <div class="text-subtitle1 text-center">
            <nuxt-link dark to="/dashboard/profile">
              Dashboard
            </nuxt-link>
          </div>
          <v-divider class="my-3" />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>

export default {
  layout: 'simple',
  head () {
    return {
      title: 'Welcome!'
    }
  }
}
</script>
