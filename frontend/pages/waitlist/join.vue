<template>
  <v-container fill-height>
    <v-row justify="center">
      <v-col cols="12" md="7" lg="6">
        <v-card align="center" elevation="10">
          <v-container class="py-7">
            <v-row justify="center" class="my-3">
              <NuxtLink to="/">
                <BigLogo max-height="35" />
              </NuxtLink>
            </v-row>
            <div class="text-h5 text-md-h4">
              Join our waitlist
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
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BigLogo from '@/components/logo/BigLogo'
import { makeSeoHeaders } from '~/assets/utils.js'

export default {
  layout: 'landing',
  components: {
    BigLogo
  },
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
      const isValid = this.$refs.form.validate()
      if (!isValid) {
        return
      }
      this.$fire.analytics.logEvent('join_waitlist')
      const payload = {
        email: this.email,
        referree_id: this.referreeCode,
        first_name: this.firstName
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

  },
  head () {
    const title = 'Join the Two Cents waitlist today!'
    return {
      title: 'Join our Waitlist',
      meta: makeSeoHeaders(title)
    }
  }
}
</script>
