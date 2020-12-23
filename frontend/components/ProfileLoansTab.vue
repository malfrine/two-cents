<template>
  <div>
    <div class="row mb-4">
      <button
        type="button"
        class="btn btn-primary ml-3"
        data-toggle="modal"
        data-target="#newLoanModal"
      >
        <!-- <font-awesome-icon icon="plus" /> -->
        <v-icon>mdi-plus</v-icon>
      </button>
    </div>
    <div class="row">
      <loan-card
        v-for="loan in loans"
        :key="loan.id"
        :loan-id="loan.id"
      />
    </div>
    <loan-modal modal-name="newLoanModal" :loan-id="null" />
  </div>
</template>

<script>
import LoanCard from './LoanCard.vue'
import LoanModal from './LoanModal.vue'

export default {
  components: { LoanCard, LoanModal },
  computed: {
    loans () {
      return this.$store.getters['finances/getLoans']
    }
  }
}
</script>
