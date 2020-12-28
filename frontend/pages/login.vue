<template>
  <div>
    <v-container class="pb-9">
      <v-row justify="center">
        <v-col cols="12" md="6" lg="5">
          <v-card elevation="15">
            <v-img
              src="/big-logo-dark.png"
            />
            <div class="text-h5 text-center">
              Login
            </div>
            <v-divider />

            <v-container>
              <v-text-field
                v-model="email"
                label="Email"
                outlined
                type="email"
              />
              <v-text-field
                v-model="password"
                label="Password"
                outlined
                type="password"
              />
              <v-row justify="center">
                <v-btn color="accent" :disabled="loggingIn" @click.prevent="handleSubmit">
                  Login
                </v-btn>
                <img
                  v-show="loggingIn"
                  src="data:image/gif;base64,R0lGODlhEAAQAPIAAP///wAAAMLCwkJCQgAAAGJiYoKCgpKSkiH/C05FVFNDQVBFMi4wAwEAAAAh/hpDcmVhdGVkIHdpdGggYWpheGxvYWQuaW5mbwAh+QQJCgAAACwAAAAAEAAQAAADMwi63P4wyklrE2MIOggZnAdOmGYJRbExwroUmcG2LmDEwnHQLVsYOd2mBzkYDAdKa+dIAAAh+QQJCgAAACwAAAAAEAAQAAADNAi63P5OjCEgG4QMu7DmikRxQlFUYDEZIGBMRVsaqHwctXXf7WEYB4Ag1xjihkMZsiUkKhIAIfkECQoAAAAsAAAAABAAEAAAAzYIujIjK8pByJDMlFYvBoVjHA70GU7xSUJhmKtwHPAKzLO9HMaoKwJZ7Rf8AYPDDzKpZBqfvwQAIfkECQoAAAAsAAAAABAAEAAAAzMIumIlK8oyhpHsnFZfhYumCYUhDAQxRIdhHBGqRoKw0R8DYlJd8z0fMDgsGo/IpHI5TAAAIfkECQoAAAAsAAAAABAAEAAAAzIIunInK0rnZBTwGPNMgQwmdsNgXGJUlIWEuR5oWUIpz8pAEAMe6TwfwyYsGo/IpFKSAAAh+QQJCgAAACwAAAAAEAAQAAADMwi6IMKQORfjdOe82p4wGccc4CEuQradylesojEMBgsUc2G7sDX3lQGBMLAJibufbSlKAAAh+QQJCgAAACwAAAAAEAAQAAADMgi63P7wCRHZnFVdmgHu2nFwlWCI3WGc3TSWhUFGxTAUkGCbtgENBMJAEJsxgMLWzpEAACH5BAkKAAAALAAAAAAQABAAAAMyCLrc/jDKSatlQtScKdceCAjDII7HcQ4EMTCpyrCuUBjCYRgHVtqlAiB1YhiCnlsRkAAAOwAAAAAAAAAAAA=="
                >
              </v-row>
            </v-container>
            <v-divider class="my-1" />
            <v-row class="mx-4 py-2" align="center">
              <div class="text">
                <nuxt-link to="/register">
                  Register
                </nuxt-link>
              </div>
              <v-spacer />
              <div class="text">
                <nuxt-link to="/forgot-password">
                  Forgot Password?
                </nuxt-link>
              </div>
            </v-row>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
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
      console.log('Handling submit')
      this.submitted = true
      const { email, password } = this
      if (email && password) {
        this.$store.dispatch('auth/postLogin', { email, password })
      }
    }
  }
}
</script>
