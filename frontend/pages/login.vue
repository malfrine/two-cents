<template>
  <div>
    <v-container class="pb-9">
      <v-row justify="center">
        <v-col cols="12" sm="8" md="6" lg="5">
          <v-card elevation="15" class="py-2">
            <v-spacer class="my-5" />
            <v-row justify="center" class="mb-3 mt-6">
              <BigLogo />
            </v-row>
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
                <v-btn color="primary" :disabled="loggingIn" :loading="loggingIn" @click.prevent="handleSubmit">
                  Login
                </v-btn>
              </v-row>
            </v-container>
            <v-divider class="my-4" />
            <v-row class="mx-4 py-4">
              <v-col cols="12" sm="6" class="d-flex justify-center justify-sm-start">
                <v-btn small to="/register" color="accent">
                  Register
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" class="d-flex justify-center justify-sm-end">
                <v-btn small to="/forgot-password" color="accent">
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
import BigLogo from '@/components/logo/BigLogo.vue'

export default {
  layout: 'simple',
  components: {
    BigLogo
  },
  data () {
    return {
      email: '',
      password: '',
      submitted: false,
      emailRules: [
        v => !!v || 'Email is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
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
      const isValid = this.$refs.form.validate()
      if (!isValid) {
        this.$toast.error('Please fix the incorrect fields')
        return
      }
      const { email, password } = this
      if (email && password) {
        this.$store.dispatch('auth/postLogin', { email, password })
      }
    }
  }
}
</script>
