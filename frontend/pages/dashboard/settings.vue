<template>
  <v-container class="pa-5">
    <PlanUpgradeDialog
      :visible="showPlanUpgradeDialog"
      @close="showPlanUpgradeDialog=false"
      @payment-made="showPlanUpgradeDialog=false"
    />
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
                  label="Name"
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
            <v-divider class="my-3" />
            <v-row justify="center" class="mt-6">
              <v-col cols="12" sm="10">
                <v-text-field
                  v-model="detailedPlanType"
                  label="Plan Type"
                  outlined
                  disabled
                />
              </v-col>
              <v-btn
                v-if="!isPremiumPlan || isCancelledPlan"
                large
                color="primary"
                class="mb-5"
                @click.prevent="showPlanUpgradeDialog = true"
              >
                Upgrade Plan
              </v-btn>
              <v-btn
                v-if="isSubscriptionPlan && !isCancelledPlan"
                large
                color="primary"
                class="mb-5"
                @click.prevent="cancelPlan"
              >
                Cancel Plan
              </v-btn>
            </v-row>
          </v-container>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import PlanUpgradeDialog from '@/components/plan/PlanUpgradeDialog.vue'
export default {
  components: { PlanUpgradeDialog },
  middleware: 'auth',
  layout: 'dashboard',
  data () {
    return {
      emailing: false,
      showPlanUpgradeDialog: false
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
    },
    planType () {
      return this.$store.getters['finances/getVerbosePlanType']
    },
    isPremiumPlan () {
      return this.$store.getters['finances/getIsPremiumPlan']
    },
    isSubscriptionPlan () {
      return this.$store.getters['finances/getIsSubscriptionPlan']
    },
    isCancelledPlan () {
      return this.$store.getters['finances/getIsCancelledPlan']
    },
    detailedPlanType () {
      if (this.isCancelledPlan) {
        return this.planType + ' (cancelled)'
      } else {
        return this.planType
      }
    }
  },
  methods: {
    sendResetPasswordEmail () {
      this.emailing = true
      this.$fire.auth.sendPasswordResetEmail(this.email)
        .then(() => {
          this.$toast.success('Please check your email to reset your password')
          this.$fire.analytics.logEvent('reset_password')
        })
        .catch((e) => {
          this.$toast.error(e.message)
        })
      this.emailing = false
    },
    async cancelPlan () {
      try {
        this.$fire.analytics.logEvent('cancel_plan')
        const paymentPlan = await this.$axios.$delete('/api/my/payment-plan')
        this.$store.commit('finances/SET_PAYMENT_PLAN', paymentPlan)
        this.$toast.success('Successfully cancelled plan')
      } catch (err) {
        this.$toast.error('Looks like something went wrong, please try again')
      }
    }
  }
}
</script>
