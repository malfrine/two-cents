<template>
  <BaseDialog
    :visible="showDialog"
    title="Build your own financial plan in less than 1 minute!"
    submit-text="Get Started"
    @close="close"
    @submit="registerUserAndClose"
  >
    <template v-slot:form>
      <v-form ref="register">
        <v-text-field
          v-model="name"
          label="Name"
          outlined
          type="string"
          :rules="[mandatoryField('Name')]"
        />
        <v-text-field
          v-model="email"
          label="Email"
          outlined
          type="email"
          :rules="[mandatoryField('Email'), emailRule()]"
        />
        <v-text-field
          v-model.trim="password"
          label="Password"
          outlined
          type="password"
          :rules="[mandatoryField('Password'), v => v.length >= 8 || 'Password must have at least 8 characters']"
        />
        <v-text-field
          v-model.trim="confirmPassword"
          label="Confirm Password"
          outlined
          type="password"
          :rules="[mandatoryField('Password')]"
        />
      </v-form>
    </template>
  </BaseDialog>
</template>

<script>
import BaseDialog from '@/components/base/BaseDialog.vue'
import { mandatoryField, emailRule } from '~/assets/rules.js'

export default {
  components: {
    BaseDialog
  },
  props: {
    showDialog: {
      type: Boolean,
      default: false
    },
    publishedPlanId: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    registerUserAndClose () {
      if (!this.$refs.register.validate()) {
        return
      }
      if (this.password !== this.confirmPassword) {
        this.$toast.error('Passwords do not match')
        return
      }
      const userInfo = {
        published_plan_id: this.publishedPlanId,
        account: {
          first_name: this.name,
          email: this.email,
          password: this.password
        }
      }
      this.$axios.post(
        '/api/my/account/onboard/from-published-plan', userInfo
      )
        .then(
          () => {
            this.$fire.auth.signOut() // just in case they were signed in as someone else
            this.$router.push('/login')
            this.$fire.analytics.logEvent('onboarded_user')
          }
        )
        .catch((e) => {
          this.$toast.error('Sorry, could not register your account')
          this.$sentry.captureException('Failed to onboard user', userInfo)
        })
      console.log('registered user')
      this.$emit('close')
    },
    close () {
      console.log('closing prompt')
      this.$emit('close')
    },
    mandatoryField,
    emailRule
  }
}
</script>
