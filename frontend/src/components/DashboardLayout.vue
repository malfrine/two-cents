<template>
  <body class="dashboard-layout">
    <dashboard-layout-side-nav></dashboard-layout-side-nav>
    <div class="main-content">
      <slot></slot>
    </div>
  </body>
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
