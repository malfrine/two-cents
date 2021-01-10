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
              Register
            </div>
            <v-divider class="my-6" />
            <v-container>
              <v-text-field
                v-model="firstname"
                label="First Name"
                outlined
              />
              <v-text-field
                v-model="lastname"
                label="Last Name"
                outlined
              />
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
              <v-text-field
                v-model="confirmPassword"
                label="Confirm Password"
                outlined
                type="password"
              />
              <v-row justify="center" class="my-3">
                <v-btn color="primary" @click.prevent="handleSubmit">
                  Register
                </v-btn>
              </v-row>
            </v-container>
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
      firstname: '',
      lastname: '',
      email: '',
      password: '',
      confirmPassword: '',
      submitted: false
    }
  },
  methods: {
    validData () {
      return (this.email && this.password.trim() === this.confirmPassword.trim())
    },
    handleSubmit (e) {
      this.submitted = true
      if (this.validData()) {
        const { email, password, firstname, lastname } = this
        this.$store.dispatch('auth/postRegister', { email, password, first_name: firstname, last_name: lastname })
      }
    }
  }
}
</script>
