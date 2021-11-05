<template>
  <div>
    <v-container class="pb-9">
      <v-row justify="center" align="center">
        <v-col
          cols="12"
          sm="8"
          md="6"
          lg="5"
        >
          <BaseFormCard title="">
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
            <v-row justify="center" class="my-4">
              <v-btn x-large color="primary" :disabled="loggingIn" :loading="loggingIn" @click.prevent="login">
                Login
              </v-btn>
            </v-row>
            <v-divider class="mb-4 mt-10" />
            <v-row>
              <v-col cols="12" class="d-flex justify-center">
                <v-btn to="/onboard" color="accent">
                  Register
                </v-btn>
              </v-col>
              <v-col cols="12" class="d-flex justify-center">
                <v-btn to="/forgot-password" color="accent">
                  Forgot Password
                </v-btn>
              </v-col>
            </v-row>
          </BaseFormCard>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>

export default {
  layout: 'simple',
  components: {
  },
  data () {
    return {
      email: '',
      password: '',
      loggingIn: false,
      emailRules: [
        v => !!v || 'Email is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w+)+$/.test(v) || 'E-mail must be valid'
      ],
      passwordRules: [
        v => !!v || 'Password is required'
      ]
    }
  },
  computed: {
    isLoggedIn () {
      return this.$store.getters['firebase-auth/isLoggedIn']
    }
  },
  watch: {
    isLoggedIn () {
      if (this.isLoggedIn) {
        this.$fire.analytics.logEvent('login')
        this.$router.push('/dashboard/profile')
      }
    }
  },
  created () {
    if (this.isLoggedIn) {
      this.$fire.analytics.logEvent('login')
      this.$router.push('/dashboard/profile')
    }
  },
  methods: {
    async login () {
      try {
        await this.$fire.auth.signInWithEmailAndPassword(
          this.email,
          this.password
        )
      } catch (e) {
        this.$toast.error(e.message)
      }
    }
  }
}
</script>
