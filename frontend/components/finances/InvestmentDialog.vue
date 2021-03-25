<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card align="center">
      <v-col cols="12" md="10">
        <div class="text-h6">
          Tell us about your investment
        </div>
        <v-divider class="my-5" />
        <v-form ref="form">
          <v-select
            v-model="investment_type"
            label="Pick your investment type"
            solo
            outlined
            item-color="primary"
            :items="investmentTypes"
            :rules="[v => !!v || 'Must provide Investment Type']"
          />
          <v-select
            v-if="isGuaranteedInvestment"
            v-model="interest_type"
            label="Pick your interest type"
            solo
            outlined
            item-color="primary"
            :items="interestTypes"
            :rules="[mandatoryFieldRule('interest_type', 'interest type')]"
          />
          <v-divider v-if="investment_type !== null" class="mb-7" />
          <v-text-field
            v-if="requiredFields.includes('name')"
            v-model="name"
            label="Investment Name"
            outlined
            :rules="[mandatoryFieldRule('name', 'investment name')]"
          />
          <v-text-field
            v-if="requiredFields.includes('current_balance')"
            v-model="current_balance"
            label="Current Balance"
            prefix="$"
            outlined
            :rules="[mandatoryFieldRule('current_balance', 'current balance')]"
          />
          <v-autocomplete
            v-if="requiredFields.includes('risk_level')"
            v-model="risk_level"
            label="Risk Level"
            :items="riskLevels"
            outlined
            :rules="[mandatoryFieldRule('risk_level', 'risk level')]"
          />
          <v-text-field
            v-if="requiredFields.includes('pre_authorized_monthly_contribution')"
            v-model="pre_authorized_monthly_contribution"
            label="Pre-Auhtorized Monthly Contribution"
            prefix="$"
            outlined
            :rules="[mandatoryFieldRule('pre_authorized_monthly_contribution', 'pre-authorized monthly contribution')]"
          />
          <v-text-field
            v-if="showRoi"
            v-model="expected_roi"
            label="Expected Return On Investment"
            suffix="%"
            outlined
            :rules="[mandatoryFieldRule('expected_roi', 'expected return on investment')]"
          />
          <v-text-field
            v-else-if="isVariable"
            v-model="prime_modifier"
            label="Expected Return On Investment"
            prefix="Prime +"
            suffix="%"
            outlined
            :rules="[mandatoryFieldRule('prime_modifier', 'expected return on investment')]"
          />
          <v-text-field
            v-if="requiredFields.includes('symbol')"
            v-model="symbol"
            label="Ticker Symbol"
            outlined
            :rules="[mandatoryFieldRule('symbol', 'ticker symbol')]"
          />
          <v-autocomplete
            v-if="requiredFields.includes('volatility_choice')"
            v-model="volatility_choice"
            label="Volatility"
            :items="volatilityChoices"
            outlined
            :rules="[mandatoryFieldRule('volatility_choice', 'volatility')]"
          />
          <v-autocomplete
            v-if="requiredFields.includes('account_type')"
            v-model="account_type"
            label="Account Type"
            :items="accountTypes"
            outlined
            :rules="[mandatoryFieldRule('account_type', 'account type')]"
          />
          <v-text-field
            v-if="isGuaranteedInvestment"
            v-model="principal_investment_amount"
            label="Principal Investment Amount"
            outlined
            :rules="[mandatoryFieldRule('principal_investment_amount', 'principal_investment_amount')]"
          />
          <v-text-field
            v-if="isGuaranteedInvestment"
            v-model="investment_date"
            label="Investment Date"
            type="date"
            outlined
            :rules="[mandatoryFieldRule('investment_date', 'investment date')]"
          />
          <v-text-field
            v-if="isGuaranteedInvestment"
            v-model="maturity_date"
            label="Maturity Date"
            type="date"
            outlined
            :rules="[mandatoryFieldRule('maturity_date', 'maturity date')]"
          />
        </v-form>
        <v-card-actions class="justify-center my-3">
          <v-btn x-large color="primary" @click.stop="createOrUpdateInvestment()">
            Save Investment
          </v-btn>
        </v-card-actions>
      </v-col>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: ['visible', 'investmentId'],
  data () {
    const investment = this.$store.getters['finances/getInvestmentById'](this.investmentId)
    if (investment) {
      console.log({ ...investment })
      return {
        id: investment.id,
        name: investment.name,
        current_balance: investment.current_balance,
        investment_type: investment.investment_type,
        pre_authorized_monthly_contribution: investment.pre_authorized_monthly_contribution,
        risk_level: investment.risk_level,
        principal_investment_amount: investment.principal_investment_amount,
        investment_date: investment.investment_date,
        maturity_date: investment.maturity_date,
        interest_type: investment.interest_type,
        prime_modifier: investment.prime_modifier,
        expected_roi: investment.expected_roi,
        symbol: investment.symbol,
        volatility_choice: investment.volatility_choice
      }
    } else {
      return {
        id: null,
        name: null,
        current_balance: null,
        investment_type: null,
        pre_authorized_monthly_contribution: null,
        risk_level: null,
        principal_investment_amount: null,
        investment_date: null,
        maturity_date: null,
        interest_type: null,
        prime_modifier: null,
        expected_roi: null,
        symbol: null,
        volatility_choice: null
      }
    }
  },
  computed: {
    show: {
      get () {
        return this.visible
      },
      set (value) {
        if (!value) {
          this.$emit('close')
        }
      }
    },

    // enums
    investmentTypes () {
      return this.$store.getters['enums/getInvestmentTypes']
    },
    riskLevels () {
      return this.$store.getters['enums/getRiskLevels']
    },
    volatilityChoices () {
      return this.$store.getters['enums/getVolatilityChoices']
    },
    requiredFields () {
      return this.$store.getters['enums/getRequiredFields'](this.investment_type)
    },
    interestTypes () {
      return this.$store.getters['enums/getInterestTypes']
    },
    accountTypes () {
      return this.$store.getters['enums/getInvestmentAccountTypes']
    },

    // attrs
    isFixed () {
      if (!this.showDetails) {
        return false
      } else {
        return this.interest_type.toUpperCase() === 'FIXED'
      }
    },
    isVariable () {
      return this.interest_type !== null && this.interest_type.toUpperCase() === 'VARIABLE'
    },
    isGuaranteedInvestment () {
      return this.requiredFields.includes('principal_investment_amount')
    },
    showRoi () {
      if (this.isGuaranteedInvestment) {
        return this.interest_type !== null && !this.isVariable
      } else {
        return this.requiredFields.includes('expected_roi')
      }
    }
  },
  methods: {
    validateInvestment () {
      const isValidForm = this.$refs.form.validate()
      return isValidForm
    },
    createOrUpdateInvestment () {
      const isValidInvestment = this.validateInvestment()
      if (!isValidInvestment) {
        return // don't submit if does not pass validation or contain error
      }
      this.show = false
      this.$store.dispatch('finances/createOrUpdateInvestment', this.makeInvestment())
    },
    makeInvestment () {
      return {
        id: this.id,
        name: this.name,
        current_balance: this.current_balance || 0,
        investment_type: this.investment_type,
        pre_authorized_monthly_contribution: this.pre_authorized_monthly_contribution || 0,
        risk_level: this.risk_level,
        principal_investment_amount: this.principal_investment_amount || 0,
        investment_date: this.investment_date,
        maturity_date: this.maturity_date,
        interest_type: this.interest_type,
        prime_modifier: this.prime_modifier,
        expected_roi: this.expected_roi,
        symbol: this.symbol,
        volatility_choice: this.volatility_choice
      }
    },
    mandatoryFieldRule (fieldName, verboseName) {
      if (this.requiredFields.includes(fieldName)) {
        return v => v !== null || `Must provide ${verboseName}`
      } else {
        return v => true
      }
    }
  }
}
</script>
