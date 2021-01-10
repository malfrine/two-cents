<template>
  <base-instrument-card>
    <template v-slot:fixed>
      <v-row class="mx-3">
        <v-card-subtitle class="mb-n7">
          <div class="text-h6">
            {{ loan.name }}
          </div>
        </v-card-subtitle>
        <v-spacer />
        <v-speed-dial
          v-model="fab"
          direction="bottom"
          class="mt-2"
        >
          <template v-slot:activator>
            <v-btn
              v-model="fab"
              icon
              fab
              small
            >
              <v-icon v-if="fab">
                mdi-close
              </v-icon>
              <v-icon v-else>
                mdi-dots-horizontal
              </v-icon>
            </v-btn>
          </template>
          <v-btn
            fab
            small
            color="blue"
            @click.stop="showLoanDialog=true"
          >
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            fab
            small
            color="red"
            @click.prevent="deleteLoan(loan)"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-speed-dial>

        <LoanDialog :visible="showLoanDialog" :loan-id="loan.id" @close="showLoanDialog=false" />
      </v-row>
      <v-card-title>
        <div class="text-h2 primary--text" color="primary">
          $ {{ loan.current_balance }}
        </div>
      </v-card-title>
    </template>
    <template v-slot:hidden>
      <v-card-text>
        <p class="mt-n5">
          {{ loan.apr }}% <em>APR</em>
        </p>
        <p class="mt-n3">
          <em>Minimum Payment:</em> ${{ loan.minimum_monthly_payment }}
        </p>
        <p class="mt-n3">
          <em>Due:</em> {{ loan.end_date }}
        </p>
      </v-card-text>
    </template>
  </base-instrument-card>
</template>

<script>
import { mapActions } from 'vuex'
import LoanDialog from '@/components/finances/LoanDialog.vue'

export default {
  components: {
    LoanDialog
  },
  props: ['loanId'],
  data () {
    return {
      showLoanDialog: false,
      showAllInfo: false,
      fab: false
    }
  },

  methods: {
    ...mapActions('finances', ['deleteLoan'])
  },
  computed: {
    loan () {
      return this.$store.getters['finances/getLoanById'](this.loanId)
    }
  }
}
</script>
