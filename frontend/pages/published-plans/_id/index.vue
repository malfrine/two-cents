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
  layout: 'published-plan',
  created () {
    const newRoute = `/published-plans/${this.$route.params.id}/plan`
    this.$router.push(newRoute)
  }
}
</script>
