<template>
  <div>
    <v-sheet elevation="4" rounded>
      <div ref="cardRef" class="mt-3 mb-1 pa-2" />
    </v-sheet>
    <v-btn color="primary" block :loading="loading" @click="purchase">
      Upgrade Now
    </v-btn>
  </div>
</template>

<script>
export default {
  props: {
    subscriptionType: {
      required: true,
      type: String
    },
    promotionCode: {
      type: String,
      default: ''
    }
  },
  data () {
    return {
      loading: false,
      token: null,
      cardStyle: {
        iconStyle: 'solid',
        style: {
          base: {
            iconColor: '#25b245',
            fontWeight: 500,
            fontFamily: 'Roboto, Open Sans, Segoe UI, sans-serif',
            fontSize: '20px',
            fontSmoothing: 'antialiased',
            padding: '2px',
            color: '#25b245',
            ':-webkit-autofill': {
              color: '#25b245'
            },
            '::placeholder': {
              color: '#25b245'
            }
          },
          invalid: {
            iconColor: '#e33a53',
            color: '#e33a53'
          }
        }

      }
    }
  },
  beforeDestroy () {
    this.$refs.cardRef?.element?.destroy()
    this.card.destroy()
  },
  mounted () {
    const card = this.$stripe.elements().create('card', this.cardStyle)
    card.mount(this.$refs.cardRef)
    this.card = card
  },
  methods: {
    async purchase () {
      this.loading = true
      try {
        const paymentPlanIntent = await this.$axios.$post(
          '/api/my/payment-plan/intent',
          {
            plan_type: this.subscriptionType,
            promotion_code: this.promotionCode
          }
        )
        const result = await this.$stripe.confirmCardPayment(
          paymentPlanIntent.client_secret,
          { payment_method: { card: this.card } }
        )
        if (result.error) {
          throw new Error('Could not confirm card payment')
        }
        const paymentPlan = await this.$axios.$post(
          '/api/my/payment-plan',
          { plan_payment_intent: paymentPlanIntent }
        )
        this.$store.commit('users/SET_PAYMENT_PLAN', paymentPlan)
        this.$toast.success('Payment successful')
        this.card.clear()
        this.$emit('payment-made')
      } catch (err) {
        this.$toast.error('Looks like something went wrong, please try again')
      }
      this.loading = false
      this.$fire.analytics.logEvent('payment')
    }
  }
}
</script>
