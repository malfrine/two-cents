<template>
  <nav
    id="sidenav-main"
    class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light bg-gradient-white"
  >
    <div class="container-fluid">
      <!-- Toggler -->
      <button
        class="navbar-toggler"
        type="button"
        data-toggle="collapse"
        data-target="#sidenav-collapse-main"
        aria-controls="sidenav-main"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon" />
      </button>
      <!-- Brand -->
      <a class="navbar-brand pt-0" href="/">
        <img
          src="@/static/logo-black.png"
          class="navbar-brand-img"
          alt="..."
        >
      </a>
      <!-- Collapse -->
      <div id="sidenav-collapse-main" class="collapse navbar-collapse">
        <!-- Collapse header -->
        <div class="navbar-collapse-header d-md-none">
          <div class="row">
            <div class="col-6 collapse-brand" />
            <div class="col-6 collapse-close">
              <button
                type="button"
                class="navbar-toggler"
                data-toggle="collapse"
                data-target="#sidenav-collapse-main"
                aria-controls="sidenav-main"
                aria-expanded="false"
                aria-label="Toggle sidenav"
              >
                <span />
                <span />
              </button>
            </div>
          </div>
        </div>
        <!-- Navigation -->
        <ul class="navbar-nav">
          <li class="nav-item">
            <nuxt-link to="/dashboard/profile" class="nav-link">
              <v-icon>mdi-badge-account-horizontal-outline</v-icon>
              User profile
            </nuxt-link>
          </li>

          <li class="nav-item">
            <nuxt-link to="/dashboard/plan" class="nav-link primary">
              <v-icon>mdi-finance</v-icon>
              Plan
            </nuxt-link>
          </li>

          <li class="nav-item">
            <nuxt-link to="/" class="nav-link primary">
              <v-icon>mdi-home</v-icon>
              Home
            </nuxt-link>
          </li>

          <li class="nav-item">
            <nuxt-link to="/goodbye" class="nav-link" @click.native="postLogout">
              <v-icon>mdi-logout</v-icon>
              Logout
            </nuxt-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  methods: {
    ...mapActions('auth', ['postLogout'])
  }
}
</script>
