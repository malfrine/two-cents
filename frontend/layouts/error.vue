<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="7" lg="5">
        <v-card>
          <v-container class="py-7">
            <v-row justify="center" class="my-3">
              <BigLogo max-height="35" />
            </v-row>
            <div class="text-subtitle-1 text-center mb-5">
              Uh-oh! Looks like there was an error...
            </div>
            <div v-if="error.statusCode === 404" class="text-h5 text-center">
              {{ pageNotFound }}
            </div>
            <div v-else class="text-h5 text-center">
              {{ otherError }}
            </div>
            <v-divider class="my-9" />
            <NuxtLink to="/">
              <div class="text-subtitle1 text-center">
                Home page
              </div>
            </NuxtLink>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BigLogo from '@/components/logo/BigLogo.vue'

export default {
  layout: 'simple',
  components: {
    BigLogo
  },
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      pageNotFound: '404 Not Found',
      otherError: 'An error occurred',
      forwardingRegex: {
        '/published-plans/{}/': 'published-plans/{}/profile'
      }
    }
  },
  created () {
    this.$sentry.captureException('An error occured on the frontend', this.error)
  },
  head () {
    const title =
      this.error.statusCode === 404 ? this.pageNotFound : this.otherError
    return {
      title
    }
  }
}
</script>

<style scoped>
h1 {
  font-size: 20px;
}
</style>
