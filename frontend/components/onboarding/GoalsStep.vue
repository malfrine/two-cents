<template>
  <v-form>
    <v-container>
      <v-stepper
        v-model="currentStep"
        vertical
      >
        <v-stepper-step
          :complete="currentStep > 1"
          step="1"
        >
          When would you like to retire?
        </v-stepper-step>
        <v-stepper-content step="1">
          <BaseQuestion
            @continue="currentStep++"
            @back="$emit('back')"
          >
            <v-text-field
              v-model="retirementAge"
              outlined
              type="Number"
            />
          </BaseQuestion>
        </v-stepper-content>

        <v-stepper-step
          :complete="currentStep > 2"
          step="2"
        >
          How much have saved up for your nest egg fund?
          <small v-if="currentStep == 2" class="mt-2">Your nest egg (or rainy day fund) is how much cash you have saved up for the sole purpose of emergency expenses</small>
        </v-stepper-step>
        <v-stepper-content step="2">
          <BaseQuestion
            @continue="currentStep++"
            @back="currentStep--"
          >
            <v-text-field
              v-model="currentNestEggAmount"
              outlined
              type="Number"
            />
          </BaseQuestion>
        </v-stepper-content>

        <v-stepper-step
          :complete="currentStep > 3"
          step="3"
        >
          Are you saving up for a big purchase?
        </v-stepper-step>
        <v-stepper-content step="3">
          <BaseQuestion
            @continue="currentStep++"
            @back="currentStep--"
          >
            <v-text-field
              v-model="nextBigPurchaseDate"
              outlined
              type="date"
            />
            <v-text-field
              v-model="nextBigPurchaseAmount"
              outlined
              type="Number"
            />
          </BaseQuestion>
        </v-stepper-content>
      </v-stepper>
    </v-container>
  </v-form>
</template>

<script>
import BaseQuestion from '@/components/onboarding/BaseQuestion.vue'

export default {
  components: {
    BaseQuestion
  },
  data () {
    const now = new Date()
    const fiveYearsFromToday = new Date(now.getFullYear() + 1, now.getMonth(), now.getDate())
    return {
      retirementAge: 65,
      currentNestEggAmount: 20000,
      nextBigPurchaseAmount: 10000,
      nextBigPurchaseDate: fiveYearsFromToday,
      currentStep: 1
    }
  },
  computed: {
    riskToleranceItems () {
      return Object.keys(this.riskToleranceObject)
    },
    goals () {
      return {
        retirement_age: this.retirementAge,
        target_nest_egg_amount: this.targetNestEggAmount,
        next_big_purchase_amount: this.nextBigPurchaseAmount,
        next_big_purchase_date: this.nextBigPurcahseDate
      }
    }
  }
}
</script>

<style scoped>
.v-text-field{
  max-width: 500px;
}
</style>
