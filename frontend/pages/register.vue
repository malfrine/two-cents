<template>
  <div>
    <v-container class="pb-9">
      <v-row justify="center">
        <v-col
          cols="12"
          sm="8"
          md="6"
          lg="5"
        >
          <BaseFormCard title="Sign Up">
            <v-form ref="form">
              <v-text-field
                v-model="firstname"
                label="First Name"
                outlined
                :rules="[v => !!v || 'First name is required']"
              />
              <v-text-field
                v-model="lastname"
                label="Last Name"
                outlined
                :rules="[v => !!v || 'Last name is required']"
              />
              <v-text-field
                v-model="email"
                label="Email"
                outlined
                type="email"
                :rules="[v => !!v || 'Email is required']"
              />
              <v-text-field
                v-model="password"
                label="Password"
                outlined
                type="password"
                :rules="[v => !!v || 'Pasword is required']"
              />
              <v-text-field
                v-model="confirmPassword"
                label="Confirm Password"
                outlined
                type="password"
                :rules="[v => !!v || 'Password is required']"
              />
            </v-form>
            <v-row justify="center" class="my-3">
              <v-btn x-large color="primary" @click.prevent="registerUser">
                Register
              </v-btn>
            </v-row>
          </BaseFormCard>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import BaseFormCard from '@/components/base/BaseFormCard.vue'

export default {
  layout: 'simple',
  components: {
    BaseFormCard
  },
  data () {
    return {
      firstname: '',
      lastname: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    validateForm () {
      if (!this.$refs.form.validate()) {
        return false
      }
      return (this.email && this.password.trim() === this.confirmPassword.trim())
    },
    registerUser () {
      if (this.validateForm()) {
        const { email, password, firstname, lastname } = this
        const payload = { email, password: password.trim(), first_name: firstname, last_name: lastname }
        try {
          this.$axios.$post('/api/my/account/', payload)
            .then((response) => {
              if (response.status === 210) {
                // Internal server error
                this.$toast.error('Sorry, could not register your account')
              } else {
                this.$router.push('/login')
              }
            })
            .catch((e) => { this.$toast.error('Sorry, could not register your account') })
        } catch (e) {
          alert(e)
        }
      }
    }
  }
}
</script>
