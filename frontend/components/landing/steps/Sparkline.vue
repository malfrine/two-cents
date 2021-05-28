<template>
  <client-only>
    <v-sparkline
      :value="value"
      :gradient="gradient"
      :smooth="radius || false"
      :padding="padding"
      :line-width="width"
      :stroke-linecap="lineCap"
      :gradient-direction="gradientDirection"
      :fill="fill"
      :type="type"
      :auto-line-width="autoLineWidth"
      auto-draw
      :height="height"
    />
  </client-only>
</template>

<script>

export default {
  data: () => ({
    fill: true,
    gradient: ['#25b245', '#135923', '#1A3D22', '#212121'],
    padding: 8,
    radius: 10,
    value: [-1, 0, 2, 5, 7, 8, 5, 10, 15, 18, 20, 24, 18, 16, 20, 15, 13, 12, -1],
    width: 2,
    lineCap: 'round',
    gradientDirection: 'top',
    type: 'trend',
    autoLineWidth: false
  }),
  computed: {
    height () {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return '200vh'
        case 'sm': return '150vh'
        case 'md': return '100%'
        case 'lg': return '100%'
        case 'xl': return '100%'
      }
      return '550px'
    }
  }
}
</script>
