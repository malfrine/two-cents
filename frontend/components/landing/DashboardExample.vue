<template>
  <div>
    <v-img
      eager
      contain
      :src="path"
      :lazy-src="lazyPath"
      :max-height="maxHeight"
      @load="loaded = true"
    />
  </div>
</template>

<script>
export default {
  props: {
    maxHeight: {
      type: String,
      default: '110'
    }
  },
  data () {
    return {
      loaded: false,
      path: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1622266448/two-cents-dashboard-v1_hrulw1.png',
      lazyPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1622267421/two-cents-dashboard-v1-lazy_zwumd2.png'
    }
  }
}
</script>
