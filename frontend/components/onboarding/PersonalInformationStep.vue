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
          What's your name?
        </v-stepper-step>
        <v-stepper-content step="1">
          <BaseQuestion
            @continue="currentStep++"
            @back="$emit('back')"
          >
            <v-text-field
              v-model="firstName"
              outlined
            />
          </BaseQuestion>
        </v-stepper-content>

        <v-stepper-step
          :complete="currentStep > 2"
          step="2"
        >
          How old are you?
        </v-stepper-step>
        <v-stepper-content step="2">
          <BaseQuestion
            @continue="currentStep++"
            @back="currentStep--"
          >
            <v-text-field
              v-model="age"
              outlined
            />
          </BaseQuestion>
        </v-stepper-content>

        <v-stepper-step
          :complete="currentStep > 3"
          step="3"
        >
          What province do you live in?
          <small v-if="currentStep == 3" class="mt-2">We use this to calculate your income taxes</small>
        </v-stepper-step>
        <v-stepper-content step="3">
          <BaseQuestion
            @continue="currentStep++"
            @back="currentStep--"
          >
            <v-autocomplete
              v-model="province"
              outlined
              :items="$constants.provinces"
            />
          </BaseQuestion>
        </v-stepper-content>

        <v-stepper-step step="4" :complete="currentStep > 4">
          What is your pre-tax monthly income?
          <small v-if="currentStep == 4" class="mt-2">We use this to determine how much you can spend each month</small>
        </v-stepper-step>
        <v-stepper-content step="4">
          <BaseQuestion
            @continue="currentStep++"
            @back="currentStep--"
          >
            <v-text-field
              v-model="preTaxMonthlySalary"
              prefix="$"
              outlined
            />
          </BaseQuestion>
        </v-stepper-content>

        <v-stepper-step step="5" :complete="currentStep > 5">
          What percent of your income do you save?
          <small v-if="currentStep == 5" class="mt-2">This is the amount of money you spend on loans (including mortages), investments, savings and any other financial goals</small>
        </v-stepper-step>
        <v-stepper-content step="5">
          <BaseQuestion
            @continue="currentStep++"
            @back="currentStep--"
          >
            <v-text-field
              v-model="savingsPercentage"
              suffix="%"
              outlined
            />
          </BaseQuestion>
        </v-stepper-content>

        <v-stepper-step step="6">
          How would you decribe your risk tolerance?
          <small v-if="currentStep == 6" class="mt-2">Your risk tolerance denotes how much money risk your willing to take for higher investment returns</small>
        </v-stepper-step>
        <v-stepper-content step="6">
          <BaseQuestion
            @continue="$emit('continue', basicInformation)"
            @back="currentStep--"
          >
            <v-radio-group v-model="riskToleranceDescription" class="mb-2 mt-n1">
              <v-radio
                v-for="(description, index) in riskToleranceItems"
                :key="index"
                :label="description"
                :value="description"
              />
            </v-radio-group>
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
    const riskToleranceObject = {
      'Play it safe always': 0,
      'Some risk never hurt anyone': 25,
      'Medium risk': 50,
      'High risk, high reward': 75,
      'Stonks only go up!': 100
    }
    return {
      firstName: null,
      province: null,
      age: null,
      preTaxMonthlySalary: null,
      riskToleranceDescription: null,
      savingsPercentage: 30,
      currentStep: 1,
      riskToleranceObject
    }
  },
  computed: {
    riskToleranceItems () {
      return Object.keys(this.riskToleranceObject)
    },
    personalInformation () {
      return {
        first_name: this.firstName,
        province: this.province,
        age: this.age,
        pre_tax_monthly_salary: this.preTaxMonthlySalary,
        risk_tolerance: this.riskToleranceObject[this.riskToleranceDescription],
        savings_percentage: this.savingsPercentage
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
