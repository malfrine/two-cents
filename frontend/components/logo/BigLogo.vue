<template>
  <div>
    <v-img
      v-if="$vuetify.theme.isDark"
      :src="darkPath"
      width="120"
      height="50"
    />
    <v-img v-else :src="lightPath" />
  </div>
</template>

<script>
export default {
  data () {
    return {
      darkPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619753012/Big%20Logos/bl-darktheme-450px_lko9ue.png',
      lightPath: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619753012/Big%20Logos/bl-lighttheme-450px_yikxbo.png'
    }
  }
}
</script>
