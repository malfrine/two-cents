<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card align="center">
      <v-col cols="12" md="10">
        <div class="text-h6">
          Tell us about your investment
        </div>
        <v-divider class="my-5" />
        <v-text-field
          v-model="localInvestment.name"
          label="Investment Name"
          outlined
        />
        <v-text-field
          v-model="localInvestment.current_balance"
          label="Current Balance"
          prefix="$"
          outlined
        />
        <v-autocomplete
          v-model="localInvestment.risk_level"
          label="Risk Level"
          :items="riskLevels"
          outlined
        />
        <v-card-actions class="justify-center">
          <v-btn x-large color="primary" @click.stop="show=false; createOrUpdateLoan()">
            Save Loan
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
    return {
      riskLevels: ['High', 'Medium', 'Low']
    }
  },
  computed: {
    localInvestment () {
      const investment = this.$store.getters['finances/getInvestmentById'](this.investmentId)
      if (investment === null) {
        return {
          name: null,
          current_balance: null,
          risk_level: null
        }
      } else {
        return { ...investment }
      }
    },
    show: {
      get () {
        return this.visible
      },
      set (value) {
        if (!value) {
          this.$emit('close')
        }
      }
    }
  },
  methods: {
    createOrUpdateLoan () {
      this.$store.dispatch('finances/createOrUpdateInvestment', this.localInvestment)
    }
  }
}
</script>
