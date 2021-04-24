<template>
  <v-card align="center">
    <v-col cols="12" md="10">
      <div class="text-h6">
        Tell us a little about yourself
      </div>
      <v-divider class="my-5" />
      <v-form ref="form">
        <v-text-field
          v-model="firstName"
          outlined
          label="First Name"
          style="max-width: 350px;"
          :rules="[v => !!v || 'First name is required']"
        />
        <v-text-field
          v-model="lastName"
          outlined
          label="Last Name (Optional)"
          style="max-width: 350px;"
        />
        <v-text-field
          v-model="email"
          outlined
          label="Your Email"
          style="max-width: 350px;"
          :rules="emailRules"
        />
        <v-card-actions class="justify-center">
          <v-btn x-large color="primary" :small="$vuetify.breakpoint.smAndDown" @click="postEmail()">
            Join Waitlist
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-col>
  </v-card>
</template>

<script>
// import { delay } from '~/assets/utils.js'

export default {
  data () {
    return {
      firstName: null,
      lastName: null,
      email: null,
      emailRules: [
        v => !!v || 'Email is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ]
    }
  },
  methods: {
    postEmail () {
      const isValid = this.$refs.form.validate()
      if (!isValid) {
        return
      }

      this.$axios.$post('/api/waitlist', { email: this.email })
        .then(
          (response) => {
            this.$toast.success('Thanks for joining our waitlist!')
            this.email = null
            this.$refs.form.reset()
          }
        )
        .catch(
          (e) => {
            this.$toast.info('This email has already been added to the waitlist!')
          }
        )
      this.$emit('form-submitted')
    }

  }
}
</script>
