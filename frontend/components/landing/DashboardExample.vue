<template>
  <div>
    <v-img
      contain
      :src="path"
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
      path: 'https://res.cloudinary.com/two-cents-ca/image/upload/v1619809865/two-cents-dashboard-v1_ydnndl.png'
    }
  }
}
</script>
