<template>
  <!-- Navbar -->
  <nav id="navbar-main" class="navbar navbar-top navbar-expand-md navbar-dark bg-gradient-primary">
    <div class="container-fluid">
      <!-- Brand -->
      <a
        class="h4 mb-0 text-white text-uppercase d-none d-lg-inline-block"
        href="/"
      >Two Cents Dashboard</a>
      <!-- User -->
      <ul class="navbar-nav align-items-center d-none d-md-flex">
        <li class="nav-item dropdown">
          <a
            class="nav-link pr-0"
            href="#"
            role="button"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          />
          <div class="dropdown-menu dropdown-menu-arrow dropdown-menu-right">
            <div class="dropdown-header noti-title">
              <h6 class="text-overflow m-0">
                Welcome!
              </h6>
            </div>
            <a href="#" class="dropdown-item">
              <i class="ni ni-single-02" />
              <span>My profile</span>
            </a>
            <a href="#" class="dropdown-item">
              <i class="ni ni-settings-gear-65" />
              <span>Settings</span>
            </a>
            <a href="#" target="_blank" class="dropdown-item">
              <i class="ni ni-support-16" />
              <span>Support</span>
            </a>
            <div class="dropdown-divider" />
            <a href="#" class="dropdown-item">
              <i class="ni ni-user-run" />
              <span>Logout</span>
            </a>
          </div>
        </li>
      </ul>
    </div>
  </nav>
  <!-- End Navbar -->
</template>

<script>
export default {}
</script>

<style>
</style>
