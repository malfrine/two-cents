<template>
  <v-form ref="form">
    <v-text-field
      v-model="email"
      outlined
      label="Your Email"
      style="max-width: 400px;"
      class="mb-n3"
    />
    <v-btn x-large color="primary" :small="$vuetify.breakpoint.smAndDown" @click="postEmail()">
      Get early access
    </v-btn>
  </v-form>
</template>

<script>
export default {
  data () {
    return {
      email: null
    }
  },
  computed: {
    referreeCode () {
      return this.$store.state.waitlist.referreeCode || ''
    }
  },
  created () {
    const referralCode = this.$route.query.referralCode
    if (!referralCode) {
      return
    }
    this.$store.commit('waitlist/SET_REFERREE_CODE', referralCode)
  },
  methods: {
    postEmail () {
      if (!this.email) {
        this.$toast.error('Please enter your email')
        return
      }
      if (!this.email.includes('@')) {
        this.$toast.error('Please enter a valid email')
        return
      }
      this.$fire.analytics.logEvent('join_waitlist')
      const payload = {
        email: this.email,
        referree_id: this.referreeCode
      }
      this.$axios.$post('/api/waitlist', payload)
        .then(
          (response) => {
            this.$store.commit('waitlist/SET_REFERRAL_CODE', response.referral_id)
            this.$router.push({ path: '/waitlist/share' })
            this.$refs.form.reset()
          }
        )
        .catch(
          (e) => {
            this.$toast.error('Sorry, we were not able to add you to the waitlist')
          }
        )
    }

  }
}
</script>
