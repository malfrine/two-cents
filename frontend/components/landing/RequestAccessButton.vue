<template>
  <v-container class="px-1 py-10">
    <v-form ref="form">
      <v-row justify="center" align="center" class="mb-n3">
        <v-text-field
          v-model="email"
          outlined
          label="Your Email"
          style="max-width: 350px;"
          :rules="emailRules"
        />
      </v-row>
      <v-row justify="center" align="center" class="mt-2">
        <v-btn x-large color="primary" :small="$vuetify.breakpoint.smAndDown" @click="postEmail()">
          Join Waitlist
        </v-btn>
      </v-row>
    </v-form>
  </v-container>
</template>

<script>
import { delay } from '~/assets/utils.js'

export default {
  data () {
    return {
      email: null,
      emailRules: [
        v => !!v || 'Email is required',
        v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || 'E-mail must be valid'
      ],
      throttlePost: false
    }
  },
  methods: {
    async postEmail () {
      const isValid = this.$refs.form.validate()
      if (!isValid || this.throttlePost) {
        return
      }
      this.$axios.$post('/api/waitlist', { email: this.email })
        .then(
          (response) => {
            this.$toast.success('Thanks for joining our waitlist!')
          }
        )
        .catch(
          (e) => {
            this.$toast.info('This email has already been added to the waitlist!')
          }
        )
      this.throttlePost = true
      await delay(5000)
      this.throttlePost = false
    }

  }
}
</script>
