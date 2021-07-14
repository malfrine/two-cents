<template>
  <BaseStep @continue="$emit('continue', financialPreferences)" @back="$emit('back')">
    <v-form>
      <v-container>
        <v-row class="mt-2">
          <v-col cols="12" md="6">
            Percent of Income Spent on Financial Goals
            <v-row align="center" align-content="center" justify="center" class="px-4 mt-4">
              <v-slider>
                <template #append>
                  100%
                </template>
                <template #prepend>
                  0%
                </template>
              </v-slider>
            </v-row>
          </v-col>
          <v-col cols="12" md="6">
            <v-autocomplete
              class="mt-3"
              outlined
              label="Risk Tolerance"
              :items="riskToleranceItems"
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
      riskToleranceItem: 'Medium Risk'
    }
  },
  computed: {
    riskToleranceItems () {
      return Object.keys(this.riskToleranceObject)
    },
    financialPreferences () {
      return {
        monthly_allowance_percent: this.monthly_allowance_percent,
        risk_tolerance_percent: this.riskToleranceObject[this.riskToleranceItem]
      }
    }
  }
}
</script>
