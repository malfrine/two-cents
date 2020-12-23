<template>
  <div>
    <body class="dashboard-layout">
      <DashboardLayoutSideNav />
      <div class="main-content">
        <nuxt />
      </div>
    </body>
    <v-footer absolute class="mt-5">
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </div>
</template>

<script>
// import DashboardLayoutTopNav from '@/components/DashboardLayoutTopNav.vue'
import DashboardLayoutSideNav from '@/components/DashboardLayoutSideNav.vue'
export default {
  components: { DashboardLayoutSideNav }
}
</script>

<style>
</style>
