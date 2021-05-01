<template>
  <div>
    <v-img
      contain
      :src="$vuetify.theme.isDark ? darkPath : lightPath"
      :max-height="maxHeight"
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
      darkPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619753012/Big%20Logos/bl-darktheme-450px_lko9ue.png',
      lightPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619753012/Big%20Logos/bl-lighttheme-450px_yikxbo.png'
    }
  }
}
</script>
