<template>
  <v-container class="pa-5">
    <v-row justify="center" align="center">
      <v-col cols="12" md="8" lg="7">
        <v-card>
          <v-container>
            <!-- Basic User Information-->
            <v-card-title class="text-h5 text-center">
              Account Information
            </v-card-title>
            <v-divider class="my-3" />
            <v-row justify="center" class="mt-6">
              <v-col cols="12" sm="10" class="mb-n6">
                <v-text-field
                  v-model="firstName"
                  label="First Name"
                  outlined
                  disabled
                />
              </v-col>
              <v-col cols="12" sm="10" class="mb-n6">
                <v-text-field
                  v-model="lastName"
                  label="Last Name"
                  outlined
                  disabled
                />
              </v-col>
              <v-col cols="12" sm="10">
                <v-text-field
                  v-model="email"
                  label="Email"
                  outlined
                  disabled
                  type="email"
                />
              </v-col>
              <v-btn
                large
                color="primary"
                class="mb-5"
                :loading="emailing"
                :disable="emailing"
                @click.prevent="sendResetPasswordEmail()"
              >
                Reset Password
              </v-btn>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  middleware: 'auth',
  layout: 'dashboard',
  data () {
    return {
      emailing: false
    }
  },
  computed: {
    firstName () {
      return this.$store.getters['finances/getFirstName']
    },
    lastName () {
      return this.$store.getters['finances/getLastName']
    },
    email () {
      return this.$store.getters['finances/getEmail']
    }
  },
  methods: {
    sendResetPasswordEmail () {
      this.emailing = true
      this.$fire.auth.sendPasswordResetEmail(this.email)
        .then(() => {
          this.$toast.success('Please check your email to reset your password')
        })
        .catch((e) => {
          this.$toast.error(e.message)
        })
      this.emailing = false
    }
  }
}
</script>
