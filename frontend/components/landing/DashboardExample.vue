<template>
  <div>
    <v-sheet color="#121212" :height="maxHeight">
      <v-container v-if="!loaded" :height="maxHeight">
        <v-card color="#121212" :height="maxHeight">
          <v-overlay absolute opacity="0">
            <v-progress-circular
              color="primary"
              indeterminate
            />
          </v-overlay>
        </v-card>
      </v-container>
      <v-img
        eager
        contain
        :src="path"
        :lazy-src="lazyPath"
        :max-height="maxHeight"
        @load="loaded = true"
      />
    </v-sheet>
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
