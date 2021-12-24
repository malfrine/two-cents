<template>
  <v-overlay z-index="2" opacity="0">
    <v-progress-circular
      :size="150"
      color="primary"
      indeterminate
    />
  </v-overlay>
</template>

<script>
export default {
  layout: 'dashboard',
  created () {
    const newRoute = '/dashboard/profile'
    this.$router.push(newRoute)
  }
}
</script>
