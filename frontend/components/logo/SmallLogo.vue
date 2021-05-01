<template>
  <div>
    <v-img
      contain
      :src="($vuetify.theme.isDark || alwaysDarkTheme) ? darkPath : lightPath"
      max-height="30"
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
      darkPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619859598/Icon%20Logos/sl-darktheme-80px_htgwur.png',
      lightPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619859598/Icon%20Logos/sl-lighttheme-80px_mzskrc.png'
    }
  }
}
</script>
