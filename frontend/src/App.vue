<template lang="html">
  <div>
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  created: function () {
    this.$store.dispatch('auth/getLoginStatus')
  }
}
</script>
