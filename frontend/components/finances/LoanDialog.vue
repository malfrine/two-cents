<template>
  <v-dialog v-model="show" max-width="500px">
    <v-card align="center">
      <v-col cols="12" md="10">
        <div class="text-h6">
          Tell us about your loan
        </div>
        <v-divider class="my-5" />
        <v-text-field
          v-model="localLoan.name"
          label="Loan Name"
          outlined
        />
        <v-text-field
          v-model="localLoan.current_balance"
          label="Current Balance"
          prefix="$"
          outlined
        />
        <v-text-field
          v-model="localLoan.apr"
          label="APR"
          suffix="%"
          outlined
        />
        <v-text-field
          v-model="localLoan.minimum_monthly_payment"
          label="Minimum Monthly Payment"
          prefix="$"
          outlined
        />
        <v-text-field
          v-model="localLoan.end_date"
          label="End Date"
          type="date"
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
  props: ['visible', 'modalName', 'loanId'],
  computed: {
    localLoan () {
      const loan = this.$store.getters['finances/getLoanById'](this.loanId)
      if (loan === null) {
        return {
          name: null,
          current_balance: null,
          apr: null,
          minimum_monthly_payment: null,
          end_date: null,
          id: null
        }
      } else {
        return { ...loan }
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
      this.$store.dispatch('finances/createOrUpdateLoan', this.localLoan)
    }
  }
}
</script>
