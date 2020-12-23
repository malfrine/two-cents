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
              <h2 class="text-center text-default">
                Login
              </h2>
            </div>
            <div class="card-body">
              <form @submit.prevent="handleSubmit">
                <div class="card-body px-lg-5 py-lg-5">
                  <div class="text-muted mb-4">
                    <div class="form-group">
                      <label for="username">Email</label>
                      <input
                        v-model="email"
                        type="text"
                        name="username"
                        class="form-control"
                        :class="{ 'is-invalid': submitted && !email }"
                      >
                      <div
                        v-show="submitted && !email"
                        class="invalid-feedback"
                      >
                        Email is required
                      </div>
                    </div>
                    <div class="form-group">
                      <label htmlFor="password">Password</label>
                      <input
                        v-model="password"
                        type="password"
                        name="password"
                        class="form-control"
                        :class="{ 'is-invalid': submitted && !password }"
                      >
                      <div
                        v-show="submitted && !password"
                        class="invalid-feedback"
                      >
                        Password is required
                      </div>
                    </div>
                    <div class="form-group" align="center">
                      <button class="btn btn-primary" :disabled="loggingIn">
                        Login
                      </button>
                      <img
                        v-show="loggingIn"
                        src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA=="
                      >
                    </div>
                  </div>
                </div>
              </form>
            </div>
            <div class="card-footer">
              <div class="text">
                <nuxt-link to="/register">
                  Register
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
  layout: 'simple',
  data () {
    return {
      email: '',
      password: '',
      submitted: false
    }
  },
  computed: {
    loggingIn () {
      return this.$store.state.auth.loggingIn
    }
  },
  created () {
    console.log('Getting login status')
    this.$store.dispatch('auth/getLoginStatus')
  },
  methods: {
    handleSubmit (e) {
      this.submitted = true
      const { email, password } = this
      if (email && password) {
        this.$store.dispatch('auth/postLogin', { email, password })
      }
    }
  }
}
</script>
