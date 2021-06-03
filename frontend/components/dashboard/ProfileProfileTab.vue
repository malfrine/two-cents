<template>
  <div>
    <v-row class="mb-4 ml-1">
      <v-btn
        fab
        large
        color="primary"
        @click.prevent="toggleEditMode()"
      >
        <v-icon v-if="!editMode" color="white">
          mdi-pencil
        </v-icon>
        <v-icon v-else color="white">
          mdi-content-save
        </v-icon>
      </v-btn>
    </v-row>
    <div>
      <v-card>
        <v-container>
          <!-- Basic User Information-->
          <v-card-title class="text-h5">
            Basic Information
          </v-card-title>
          <v-row justify="center">
            <v-col cols="12" sm="10" md="6">
              <v-text-field
                v-model="first_name"
                label="First Name"
                outlined
                disabled
              />
            </v-col>
            <v-col cols="12" sm="10" md="6">
              <v-text-field
                v-model="last_name"
                label="Last Name"
                outlined
                disabled
              />
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="12" sm="10" md="6">
              <TooltipTextField
                v-model="financial_profile.birth_date"
                label="Birthdate"
                outlined
                :disabled="!editMode"
                type="date"
                tooltip-text="Your birthdate is used to calculate your TFSA and RRSP contribution limits and for retirement withdrawal planning"
              />
            </v-col>
            <v-col cols="12" sm="10" md="6">
              <v-text-field
                v-model="email"
                label="Email"
                outlined
                disabled
                type="email"
              />
            </v-col>
            <v-col cols="12" sm="10" md="6">
              <TCTooltip>
                <template v-slot:inner>
                  <v-autocomplete
                    v-model="financial_profile.province_of_residence"
                    label="Province"
                    outlined
                    :disabled="!editMode"
                    :items="provinces"
                    tooltip-text="This is the province to which you pay taxes. This information along with you income is used to determine what tax bracket you fall into"
                  />
                </template>
              </TCTooltip>
            </v-col>
          </v-row>
          <!-- Financial Information -->
          <v-divider />
          <v-card-title class="text-h5">
            Financial Information
          </v-card-title>
          <v-row justify="center">
            <v-col cols="12" sm="10" md="6">
              <TooltipTextField
                v-model="financial_profile.monthly_salary_before_tax"
                label="Pre-Tax Monthly Income"
                outlined
                prefix="$"
                :disabled="!editMode"
                tooltip-text="Pre-tax monthly income can be found on your paystub, or even in your employment offer letter."
              />
            </v-col>
            <v-col cols="12" sm="10" md="6">
              <v-text-field
                v-model="financial_profile.retirement_age"
                label="Planned Retirement Age"
                outlined
                :disabled="!editMode"
              />
            </v-col>
            <v-col cols="12" sm="10" md="6">
              <TooltipTextField
                v-model="financial_profile.starting_rrsp_contribution_limit"
                label="RRSP Contribution Limit"
                outlined
                prefix="$"
                :disabled="!editMode"
                tooltip-text="This is the amount of money you can put in your RRSP as of today. To find out your RRSP contribution limit, login to your MyCRA account at www.canada.ca, call the Canada TIPS line (1-800-267-6999), or view your RRSP information from your T1028 tax form."
              />
            </v-col>
            <v-col cols="12" sm="10" md="6">
              <TooltipTextField
                v-model="financial_profile.starting_tfsa_contribution_limit"
                label="TFSA Contribution Limit"
                outlined
                :disabled="!editMode"
                tooltip-text="This is the amount of money you can put in your TFSA as of today. To find out exactly how much you can contribute, login to your MyCRA account at www.canada.ca or call the Canada TIPS line (1-800-267-6999)."
              />
            </v-col>
          </v-row>
          <v-divider inset />
          <v-card-title>
            <TCTooltip text="The percentage of your income that you put away for long-term goals like paying off your loans and investments.">
              <template v-slot:inner>
                Percent of Income Allocated for Financial Goals
              </template>
            </TCTooltip> :
            {{ financial_profile.percent_salary_for_spending }}%
          </v-card-title>
          <v-row class="mt-6" align="center" align-content="center" justify="center">
            <v-slider v-model="financial_profile.percent_salary_for_spending" style="max-width: 500px" :disabled="!editMode">
              <template #append>
                100%
              </template>
              <template #prepend>
                0%
              </template>
            </v-slider>
          </v-row>
          <v-divider inset />
          <v-card-title>
            <TCTooltip
              text="The amount of risky investments you’re willing to take on. 0% risk tolerance means you will avoid investing until you pay off your loans and you are comfortable with the least risky investments. 100% risk tolerance means you are comfortable with the riskiest investments because it might lead to a higher return."
            >
              <template v-slot:inner>
                Risk Tolerance
              </template>
            </TCTooltip> :
            {{ financial_profile.risk_tolerance }}%
          </v-card-title>
          <v-row class="mt-n3" align="center" align-content="center" justify="center">
            <v-slider v-model="financial_profile.risk_tolerance" style="max-width: 500px" :disabled="!editMode">
              <template #append>
                100%
              </template>
              <template #prepend>
                0%
              </template>
            </v-slider>
          </v-row>
        </v-container>
      </v-card>
    </div>
  </div>
</template>

<script>
import TooltipTextField from '@/components/base/TooltipTextField.vue'
import TCTooltip from '@/components/base/TCTooltip.vue'

export default {
  components: { TooltipTextField, TCTooltip },
  data () {
    const defaultFinProfile = {
      birth_date: new Date(),
      monthly_salary_before_tax: 8000,
      starting_rrsp_contribution_limit: 0,
      starting_tfsa_contribution_limit: 0,
      retirement_age: 65,
      percent_salary_for_spending: 25,
      death_age: 90,
      province_of_residence: 'AB'
    }
    return {
      editMode: false,
      defaultFinProfile,
      financial_profile: { ...this.$store.getters['finances/getFinancialProfile'] }
    }
  },
  computed: {
    first_name () {
      return this.$store.getters['finances/getFirstName']
    },
    last_name () {
      return this.$store.getters['finances/getLastName']
    },
    email () {
      return this.$store.getters['finances/getEmail']
    },

    provinces () {
      return this.$store.getters['enums/getProvinces']
    }
  },
  methods: {
    toggleEditMode () {
      if (this.editMode) {
        const fp = { ...this.defaultFinProfile, ...this.financial_profile }
        this.$axios.$post('/api/my/finances/profile', fp)
          .then(
            (response) => {
              this.$store.commit('finances/SET_FINANCIAL_PROFILE', response)
              this.financial_profile = { ...this.$store.getters['finances/getFinancialProfile'] }
            }
          )
          .catch(
            (e) => {
              this.$toast.error('Could not update your information')
              this.financial_profile = { ...this.$store.getters['finances/getFinancialProfile'] }
            }
          )
      }
      this.editMode = !this.editMode
    }
  }
}
</script>
