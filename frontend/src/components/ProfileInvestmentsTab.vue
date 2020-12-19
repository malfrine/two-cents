<template>
  <div>
    <div class="row mb-4">
      <button
        type="button"
        class="btn btn-primary ml-3"
        data-toggle="modal"
        data-target="#newInvestmentModal"
      >
        <font-awesome-icon icon="plus"></font-awesome-icon>
      </button>
    </div>
    <div class="row">
      <investment-card
        v-for="investment in getInvestments"
        v-bind:key="investment.id"
        v-bind:investmentId="investment.id"
      >
      </investment-card>
    </div>
    <investment-modal modalName="newInvestmentModal" v-bind:investmentId="null">
    </investment-modal>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import InvestmentCard from './InvestmentCard.vue'
import InvestmentModal from './InvestmentModal.vue'

export default {
  components: { InvestmentCard, InvestmentModal },
  computed: {
    ...mapGetters('finances', ['getInvestments'])
  }
}
</script>
