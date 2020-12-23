<template>
  <div>
    <div class="container mt--8 pb-9">
      <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
          <v-card>
            <h1 class="text-center" v-if="error.statusCode === 404">
              {{ pageNotFound }}
            </h1>
            <h1 class="text-center" v-else>
              {{ otherError }}
            </h1>
            <NuxtLink class="text-center" to="/">
              Home page
            </NuxtLink>
          </v-card>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  layout: 'simple',
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      pageNotFound: '404 Not Found',
      otherError: 'An error occurred'
    }
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
