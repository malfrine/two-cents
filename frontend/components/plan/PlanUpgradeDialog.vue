<template>
  <v-dialog v-model="show" max-width="1000">
    <v-card class="pa-6">
      <v-row class="fill-height my-0" justify="center">
        <v-col cols="12" md="4">
          <div class="text-h5 mt-2">
            Why should you upgrade your plan?
          </div>
          <div class="text-caption mt-2 grey--text">
            You will get all features from the basic financial plan plus:
          </div>
          <v-container class="my-3">
            <v-row>
              <v-col
                v-for="(sellingPoint, index) in sellingPoints"
                :key="index"
                cols="12"
                sm="6"
                md="12"
              >
                <div class="text-headline">
                  <v-icon color="primary" large class="mr-2">
                    {{ sellingPoint.icon }}
                  </v-icon>
                  {{ sellingPoint.title }}
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-col>
        <v-col cols="12" md="8">
          <v-sheet class="fill-height pa-4" elevation="12">
            <div class="text-h5 text-center mt-2">
              You'll need to upgrade your plan to do that!
            </div>
            <div class="text-caption text-center grey--text">
              Choose your preferred plan
            </div>
            <v-item-group mandatory>
              <v-container>
                <v-row>
                  <v-col
                    v-for="(subscription, index) in subscriptionTypes"
                    :key="index"
                    cols="12"
                    sm="4"
                  >
                    <v-item v-slot="{ active, toggle }">
                      <v-card
                        :color="active ? 'primary' : null"
                        class="align-center py-4 px-2"
                        dark
                        @click="toggle(); setActiveIndex(index)"
                      >
                        <div class="text-h4 text-center">
                          {{ subscription.amount }}
                        </div>
                        <div class="text-subtitle1 text-center">
                          {{ subscription.frequency }}
                        </div>
                      </v-card>
                    </v-item>
                  </v-col>
                </v-row>
              </v-container>
            </v-item-group>
            <v-container>
              <div class="text-caption font-italic">
                {{ chosenSubscription.details }}
              </div>
            </v-container>
            <v-divider class="mb-1 mt-4" />
            <v-container>
              <div class="">
                Billing Information
              </div>
              <PaymentForm :subscription-type="chosenSubscription.type" @payment-made="$emit('payment-made')" />
            </v-container>
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
      activeSubscriptionIndex: 2,
      subscriptionTypes: [
        {
          name: 'One Time Fee',
          amount: '$25',
          accessDuration: '24 hours',
          details: "You'll be able to access update your plan for the next 24 hours in case you want to make any changes.",
          type: 'one-time',
          frequency: 'one time'
        },
        {
          name: 'Monthly Subscription',
          amount: '$10',
          accessDuration: '1 month',
          details: "You'll be automatically charged $10 every month for your subscription. You can update and build your plan as many times as you want. You can cancel any time.",
          type: 'monthly',
          frequency: 'monthly'
        },
        {
          name: 'Annual Subscription',
          amount: '$100',
          accessDuration: '1 year',
          details: "You'll be automatically charged $100 every year for your subscription. You can update and build your plan as many times as you want. You can cancel any time.",
          type: 'annual',
          frequency: 'annual'
        }
      ],
      sellingPoints: [
        {
          title: 'Net worth projection',
          detail: 'Get detailed projections of how your investments and loans will grow until you retire',
          icon: 'mdi-chart-areaspline'
        },
        {
          title: 'Detailed action plan',
          detail: 'Get month to month spending plans to execute your financial plan',
          icon: 'mdi-book-open'
        },
        {
          title: 'Unlimited goals',
          detail: 'Add more than 3 financial goals',
          icon: 'mdi-trophy'
        },
        {
          title: 'Unlimited loans',
          detail: 'Add more than 5 loans',
          icon: 'mdi-credit-card-multiple'
        },
        {
          title: 'Unlimited investments',
          detail: 'Add more than 5 investments',
          icon: 'mdi-rocket'
        }
      ]
    }
  },
  computed: {
    chosenSubscription () {
      return this.subscriptionTypes[this.activeSubscriptionIndex]
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
  created () {
    this.$fire.analytics.logEvent('premium_interest')
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
