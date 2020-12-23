<template>
  <div class="bg-default">
    <div class="main-content">
      <SimpleLayoutNav />

      <SimpleLayoutHeader />

      <div class="container-fluid mt--9 pb--3">
        <nuxt />
      </div>
    </div>
    <v-footer absolute>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </div>
</template>

<script>
import SimpleLayoutHeader from '@/components/SimpleLayoutHeader.vue'
import SimpleLayoutNav from '@/components/SimpleLayoutNav.vue'

export default {
  components: {
    SimpleLayoutHeader,
    SimpleLayoutNav
  }
}
</script>
