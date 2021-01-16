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
          $ {{ payment.payment }}
        </div>
      </v-row>
      <v-divider />
      <v-row class="px-6 my-2">
        <div class="text-h6">
          Monthly Allowance
        </div>
        <v-spacer class="my-2" />
        <div class="text-h6">
          $ {{ monthlyAllowance }}
        </div>
      </v-row>
    </v-card-subtitle>
  </v-card>
</template>

<script>
export default {
  props: ['selectedStrategy'],
  computed: {
    actionPlan () {
      return this.$store.getters['plan/getActionPlan'](this.selectedStrategy)
    },
    payments () {
      return this.actionPlan.payments
    },
    monthlyAllowance () {
      return this.actionPlan.monthly_allowance
    }
  }
}
</script>
