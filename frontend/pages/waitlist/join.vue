<template>
  <v-container fill-height>
    <v-row justify="center">
      <v-col cols="12" md="7" lg="6">
        <v-card align="center" elevation="10" class="mb-15">
          <v-container class="py-7">
            <v-row justify="center" class="my-3">
              <NuxtLink to="/">
                <BigLogo max-height="35" />
              </NuxtLink>
            </v-row>
            <div class="text-h5 text-md-h4">
              Get early access
            </div>
            <v-divider class="my-5" />
            <JoinWaitlistButton />
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BigLogo from '@/components/logo/BigLogo'
import JoinWaitlistButton from '@/components/landing/JoinWaitlistButton.vue'
import { makeSeoHeaders } from '~/assets/utils.js'

export default {
  layout: 'landing',
  components: {
    BigLogo,
    JoinWaitlistButton
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
