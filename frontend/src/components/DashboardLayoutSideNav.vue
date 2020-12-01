<template>
  <nav
    class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light bg-gradient-white"
    id="sidenav-main"
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
        <span class="navbar-toggler-icon"></span>
      </button>
      <!-- Brand -->
      <a class="navbar-brand pt-0" href="/">
        <img
          src="../assets/logo-black.png"
          class="navbar-brand-img"
          alt="..."
        />
      </a>
      <!-- Collapse -->
      <div class="collapse navbar-collapse" id="sidenav-collapse-main">
        <!-- Collapse header -->
        <div class="navbar-collapse-header d-md-none">
          <div class="row">
            <div class="col-6 collapse-brand"></div>
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
                <span></span>
                <span></span>
              </button>
            </div>
          </div>
        </div>
        <!-- Navigation -->
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link to="/dashboard/profile" class="nav-link">
              <font-awesome-icon
                icon="address-card"
                class="mr-2"
              ></font-awesome-icon
              >User profile
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/dashboard/plan" class="nav-link primary">
              <font-awesome-icon
                icon="chart-line"
                class="mr-2"
              ></font-awesome-icon>
              Plan
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/login" v-on:click.native="logout" class="nav-link">
              <font-awesome-icon
                icon="sign-out-alt"
                class="mr-2"
              ></font-awesome-icon>
              Logout
            </router-link>
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
    ...mapActions('authentication', ['logout'])
  }
}
</script>
