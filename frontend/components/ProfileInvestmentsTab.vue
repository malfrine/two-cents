<template>
  <div>
    <div class="row mb-4">
      <button
        type="button"
        class="btn btn-primary ml-3"
        data-toggle="modal"
        data-target="#newInvestmentModal"
      >
        <!-- <font-awesome-icon icon="plus"></font-awesome-icon> -->
        <v-icon color="primary">mdi-plus</v-icon>
      </button>
    </div>
    <div class="row">
      <investment-card
        v-for="investment in getInvestments"
        :key="investment.id"
        :investment-id="investment.id"
      />
    </div>
    <investment-modal modal-name="newInvestmentModal" :investment-id="null" />
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
