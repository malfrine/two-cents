<template>
  <div>
    <div class="row mb-4">
        <button
        type="button"
        class="btn btn-primary ml-3"
        data-toggle="modal"
        data-target="#newLoanModal"
      >
        <font-awesome-icon icon="plus"></font-awesome-icon>
      </button>
    </div>
    <div class="row">
      <loan-card
        v-for="loan in loans"
        v-bind:key="loan.id"
        v-bind:loanId="loan.id"
      >
      </loan-card>
    </div>
    <loan-modal modalName="newLoanModal" v-bind:loanId="null">
    </loan-modal>
  </div>
</template>

<script>
import LoanCard from './LoanCard.vue'
import LoanModal from './LoanModal.vue'

import { mapGetters } from 'vuex'

export default {
  components: { LoanCard, LoanModal },
  computed: {
    loans() {
      return this.$store.getters["finances/getLoans"]
    }
  }
}
</script>
