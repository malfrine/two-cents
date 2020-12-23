<template>
  <div>
    <div class="container mt--8 pb-9">
      <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
          <div class="card shadow">
            <div class="card-header">
              <img
                src="@/static/big-logo-dark.png"
                class="img-fluid"
                alt="Responsive image"
              >
              <p class="text-center text-default">
                DIY financial planning powered by AI
              </p>
            </div>
            <div class="card-footer">
              <div class="text-center">
                <nuxt-link to="/dashboard/profile">
                  Dashboard
                </nuxt-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  layout: 'simple'
}
</script>
