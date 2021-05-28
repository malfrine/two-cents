<template>
  <v-card elevation="20" dark>
    <v-carousel
      show-arrows-on-hover
      hide-delimiters
      :height="height"
      :style="`background: linear-gradient(${gradientDegree}deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%;`"
    >
      <v-carousel-item
        v-for="(url, i) in imageUrls"
        :key="i"
        :src="url"
        contain
      />
    </v-carousel>
  </v-card>
</template>

<script>
export default {
  props: {
    imageUrls: {
      type: Array,
      required: true
    },
    gradientDegree: {
      type: Number,
      default: 60
    }
  },
  computed: {
    height () {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return '300px'
        case 'sm': return '450px'
        case 'md': return '400px'
        case 'lg': return '500px'
        case 'xl': return '550px'
      }
      return '550px'
    }
  }
}
</script>

<style scoped>
.gradient {
  background: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(19,89,35,1) 32%, rgba(33,33,33,1) 67%);
}
</style>
