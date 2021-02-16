<template>
  <div>
    <v-row class="mb-4 ml-1">
      <v-btn
        fab
        large
        color="primary"
        @click.prevent="toggleEditMode()"
      >
        <v-icon v-if="!this.editMode" color="white">
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
          <v-card-title>
            User Information
          </v-card-title>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="first_name"
                label="First Name"
                outlined
                disabled
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="last_name"
                label="Last Name"
                outlined
                disabled
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="financial_profile.birth_date"
                label="Birthdate"
                outlined
                :disabled="!editMode"
                type="date"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="email"
                label="Email"
                outlined
                disabled
                type="email"
              />
            </v-col>
          </v-row>
          <!-- Financial Information -->
          <v-divider />
          <v-card-title>
            Financial Information
          </v-card-title>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="financial_profile.monthly_allowance"
                label="Monthly Allowance"
                outlined
                prefix="$"
                :disabled="!editMode"
              />
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="financial_profile.retirement_age"
                label="Planned Retirement Age"
                outlined
                :disabled="!editMode"
              />
            </v-col>
          </v-row>
          <v-divider />
          <v-card-title>
            Risk Tolerance: {{ financial_profile.risk_tolerance }}%
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

export default {
  data () {
    return {
      editMode: false,
      defaultBirthDate: new Date(),
      defaultMonthlyAllowance: 1000,
      defaultRetirementAge: 65,
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
    }
  },
  methods: {
    toggleEditMode () {
      if (this.editMode) {
        const fp = {
          birth_date: this.financial_profile.birth_date || this.defaultBirthDate,
          monthly_allowance: this.financial_profile.monthly_allowance || this.defaultMonthlyAllowance,
          retirement_age: this.financial_profile.retirement_age || this.defaultRetirementAge,
          risk_tolerance: this.financial_profile.risk_tolerance
        }
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
