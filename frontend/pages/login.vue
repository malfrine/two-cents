<template>
  <div>
    <v-container class="pb-9">
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6" lg="5">
          <v-card elevation="15">
            <v-img
              src="/big-logo-dark.png"
            />
            <div class="text-h5 text-center">
              Login
            </div>
            <v-divider class="my-7" />

            <v-container class="px-6">
              <v-form ref="form">
                <v-text-field
                  v-model="email"
                  label="Email"
                  outlined
                  type="email"
                  :rules="emailRules"
                />
                <v-text-field
                  v-model="password"
                  label="Password"
                  outlined
                  type="password"
                  :rules="passwordRules"
                />
              </v-form>
              <v-row justify="center">
                <v-btn color="accent" :disabled="loggingIn" :loading="loggingIn" @click.prevent="handleSubmit">
                  Login
                </v-btn>
              </v-row>
            </v-container>
            <v-divider class="my-4" />
            <v-row class="mx-4 py-4">
              <v-col cols="12" sm="6" class="d-flex justify-center justify-sm-start">
                <v-btn small to="/register" color="primary">
                  Register
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" class="d-flex justify-center justify-sm-end">
                <v-btn small to="/forgot-password" color="primary">
                  Forgot Password
                </v-btn>
              </v-col>
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
      submitted: false,
      emailRules: [
        v => !!v || 'Email is required'
      ],
      passwordRules: [
        v => !!v || 'Password is required'
      ]
    }
  },
  computed: {
    loggingIn () {
      return this.$store.state.auth.loggingIn
    }
  },
  created () {
    this.$store.dispatch('auth/getLoginStatus')
  },
  methods: {
    handleSubmit (e) {
      this.submitted = true
      this.$refs.form.validate()
      const { email, password } = this
      if (email && password) {
        this.$store.dispatch('auth/postLogin', { email, password })
      }
    }
  }
}
</script>
