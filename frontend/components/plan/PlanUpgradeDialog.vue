<template>
  <v-dialog v-model="show" max-width="1000">
    <v-card height="70vh" width="100vw" class="pa-3">
      <v-row class="fill-height my-0" justify="center">
        <v-col cols="4">
          // insert information and features
        </v-col>
        <v-col cols="8">
          <v-sheet elevation="12" class="fill-height">
            <v-item-group mandatory>
              <v-container>
                <v-row>
                  <v-col
                    v-for="(subscription, index) in subscriptionTypes"
                    :key="index"
                    cols="12"
                    md="4"
                  >
                    <v-item v-slot="{ active, toggle }">
                      <v-card
                        :color="active ? 'primary' : ''"
                        class="d-flex align-center fill-height"
                        dark
                        @click="toggle(); setActiveIndex(index)"
                      >
                        <v-card-title>
                          {{ subscription.amount }}
                        </v-card-title>
                      </v-card>
                    </v-item>
                  </v-col>
                </v-row>
              </v-container>
            </v-item-group>
            {{ subscriptionType }}
            <PaymentForm :subscription-type="subscriptionType" @payment-made="$emit('payment-made')" />
          </v-sheet>
        </v-col>
      </v-row>
    </v-card>
  </v-dialog>
</template>

<script>
import PaymentForm from '@/components/base/PaymentForm.vue'

export default {
  components: {
    PaymentForm
  },
  props: {
    visible: {
      required: true,
      type: Boolean
    }
  },
  data () {
    return {
      activeSubscriptionIndex: 0,
      subscriptionTypes: [
        {
          name: 'One Time Fee',
          amount: '$25 one-time',
          accessDuration: '24 hours',
          detais: "You'll be able to change and update your plan for the next 24 hours if you have any changes",
          type: 'one-time'
        },
        {
          name: 'Monthly Subscription',
          amount: '$10 / month ',
          accessDuration: '1 month',
          details: "You'll be automatically charged every month for your subscription",
          type: 'monthly'
        },
        {
          name: 'Annual Subscription',
          amount: '$100 / year',
          accessDuration: '1 year',
          details: "You'll be automatically charged every year for your subscription",
          type: 'annual'
        }
      ]
    }
  },
  computed: {
    subscriptionType () {
      return this.subscriptionTypes[this.activeSubscriptionIndex].type
    },
    // dialog functionality
    show: {
      get () {
        return this.visible
      },
      set (value) {
        if (!value) {
          this.$emit('close')
        }
      }
    }
  },
  methods: {
    setActiveIndex (index) {
      this.activeSubscriptionIndex = index
    }
  }
}
</script>

<style>
.gradient-border {
border-color: linear-gradient(60deg, rgba(37,178,69,1) 0%, rgba(53,163,87,1) 7%, rgba(68,148,105,1) 26%, rgba(84,133,124,1) 44%, rgba(100,117,142,1) 66%, rgba(115,102,160,1) 85%) 1 stretch;
}
</style>
