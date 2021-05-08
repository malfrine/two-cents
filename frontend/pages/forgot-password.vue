<template>
  <v-container class="pb-9">
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6" lg="5">
        <BaseFormCard title="Forgot Email/Password" :sub-title="subTitle">
          <slot>
            <v-form ref="form" @submit.prevent>
              <v-text-field
                v-model="email"
                label="Email"
                outlined
                type="email"
                :rules="emailRules"
                style="max-width: 300px"
              />
              <!-- Added second @submite.prevent because if you have one v-text-field
              and press enter, it will refresh the page. Bug in vue
              https://forum.framework7.io/t/vue-pressing-enter-key-in-input-causes-app-to-reload/2585/15
              -->
            </v-form>
            <v-row justify="center">
              <v-btn x-large color="primary" :disabled="emailing" :loading="emailing" @click.prevent="sendEmail">
                Email Me
              </v-btn>
            </v-row>
          </slot>
        </BaseFormCard>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import BaseFormCard from '@/components/base/BaseFormCard.vue'
import { emailRules } from '~/assets/rules.js'

export default {
  layout: 'simple',
  components: {
    BaseFormCard
  },
  data () {
    return {
      title: 'Forgot Email/Password',
      subTitle: 'We will send you an email with instructions on how to recover your password',
      emailRules,
      email: '',
      emailing: false
    }
  },
  methods: {
    sendEmail () {
      if (!this.$refs.form.validate()) {
        return
      }
      this.emailing = true
      this.$fire.auth.sendPasswordResetEmail(this.email)
        .then(() => {
          this.$toast.success('Please check your email for next steps')
        })
        .catch((e) => {
          this.$toast.error(e.message)
        })
      this.emailing = false
    }
  }
}
</script>
