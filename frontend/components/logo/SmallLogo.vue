<template>
  <div>
    <v-img
      contain
      :src="($vuetify.theme.isDark || alwaysDarkTheme) ? darkPath : lightPath"
      max-width="120"
      max-height="50"
    />
  </div>
</template>

<script>
export default {
  props: {
    alwaysDarkTheme: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      darkPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619753926/Icon%20Logos/sl-darktheme-80px_ep9rka.png',
      lightPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619753926/Icon%20Logos/sl-lighttheme-80px_ht35la.png'
    }
  }
}
</script>
