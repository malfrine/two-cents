<template>
  <BaseStep @continue="$emit('continue', investments)" @back="$emit('back')">
    <v-form>
      <v-container class="px-4">
        <v-row class="mt-2">
          <v-col cols="12" md="6">
            <v-text-field
              v-model="rrspContributionLimit"
              outlined
              label="RRSP Contribution Limit"
              type="Number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="tfsaContributionLimit"
              outlined
              label="TFSA Contribution Limit"
              type="Number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="totalHighRiskInvestments"
              outlined
              label="Total High Risk Investments"
              type="Number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="totalMediumRiskInvestments"
              outlined
              label="Total Medium Risk Investments"
              type="Number"
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="totalLowRiskInvestments"
              outlined
              label="Total Low Risk Investments"
              type="Number"
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
    return {
      rrspContributionLimit: 0,
      tfsaContributionLimit: 0,
      totalHighRiskInvestments: 0,
      totalMediumRiskInvestments: 0,
      totalLowRiskInvestments: 0
    }
  },
  computed: {
    investments () {
      return {
        rrsp_contribution_limit: this.rrspContributionLimit,
        tfsa_contribution_limit: this.tfsaContributionLimit,
        total_high_risk_investments: this.totalHighRiskInvestments,
        total_medium_risk_investments: this.totalMediumRiskInvestments,
        total_low_risk_investments: this.totalLowRiskInvestments
      }
    }
  }
}
</script>
