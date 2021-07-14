<template>
  <BaseStep @continue="$emit('continue', personalInformation)" @back="$emit('back')">
    <v-form>
      <v-container class="px-4">
        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Remaining Mortgage Balance"
              type="number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Mortage End Date"
              type="date"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Total Student Loans Balance"
              type="number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Total Student Loans Due Date"
              type="date"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Total Personal Loans Balance"
              type="number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Personal Loans Due Date"
              type="date"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Total Credit Card Debt"
              type="number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              outlined
              label="Total Line Of Credit Balance"
              type="number"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </BaseStep>
</template>

<script>
import BaseStep from '@/components/onboarding/BaseStep.vue'

export default {
  components: {
    BaseStep
  },
  data () {
    const riskToleranceObject = {
      'Play it Safe, Always': 0,
      'Some Risk Never Hurt Anyone': 25,
      'Medium Risk': 50,
      'High Risk, High Reward': 75,
      'Stonks only Go Up!': 100
    }
    return {
      riskToleranceObject,
      monthlyAllowancePercent: 20,
      risk_tolerance_item: 'Medium Risk'
    }
  },
  computed: {
    riskToleranceItems () {
      return Object.keys(this.riskToleranceObject)
    },
    personalInformation () {
      return {
        monthly_allowance_percent: this.monthly_allowance_percent
      }
    }
  }
}
</script>
