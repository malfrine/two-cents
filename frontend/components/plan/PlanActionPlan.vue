<template>
  <v-card>
    <v-card-title>
      Payment Plan for then Next 3 Months
    </v-card-title>
    <v-divider class="my-1" />
    <v-card-subtitle>
      <v-row v-for="payment in payments" :key="payment.instrument" class="px-6 my-2">
        <div class="text-h6">
          {{ payment.instrument }}
        </div>
        <v-spacer />
        <div class="text-h6">
          <div
            v-if="!isPremiumPlan"
            @click="$emit('show-upgrade-dialog')"
          >
            $XX.XX
          </div>
          <div v-else>
            {{ asDollar(payment.payment) }}
          </div>
        </div>
      </v-row>
      <v-divider />
      <v-row class="px-6 my-2">
        <div class="text-h6">
          Monthly Allowance
        </div>
        <v-spacer class="my-2" />
        <div class="text-h6">
          {{ isPremiumPlan ? asDollar(monthlyAllowance) : '$XX.XX' }}
        </div>
      </v-row>
    </v-card-subtitle>
  </v-card>
</template>

<script>
import { asDollar } from '~/assets/utils.js'

export default {
  props: {
    selectedStrategy: {
      type: String,
      required: true
    },
    isPremiumPlan: {
      type: Boolean,
      required: true
    },
    publishedPlanId: {
      type: Number,
      default: null
    }
  },
  computed: {
    actionPlan () {
      if (this.publishedPlanId != null) {
        return this.$store.getters['published-plans/getActionPlan'](this.publishedPlanId, this.selectedStrategy)
      } else {
        return this.$store.getters['plan/getActionPlan'](this.selectedStrategy)
      }
    },
    payments () {
      return this.actionPlan.payments
    },
    monthlyAllowance () {
      return this.actionPlan.monthly_allowance
    }
  },
  methods: {
    asDollar,
    getColor (payment) {
      return this.$instrument.colors.getColor(payment.instrument_type, payment.id)
    }
  }
}
</script>
