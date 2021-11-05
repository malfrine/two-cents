<template>
  <div>
    <v-row class="mb-4 ml-1">
      <v-btn
        fab
        large
        color="primary"
        @click.stop="registerAddButtonClick"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-row>
    <v-row justify="center" justify-lg="start">
      <loan-card
        v-for="loan in loans"
        :key="loan.id"
        :loan-id="loan.id"
      />
    </v-row>
    <LoanDialog :visible="showLoanDialog" :loan-id="null" @close="showLoanDialog=false" />
    <PlanUpgradeDialog
      :visible="showPlanUpgradeDialog"
      @close="showPlanUpgradeDialog=false"
      @payment-made="showPlanUpgradeDialog=false"
    />
  </div>
</template>

<script>
import LoanCard from '@/components/finances/LoanCard.vue'
import LoanDialog from '@/components/finances/LoanDialog.vue'
import PlanUpgradeDialog from '@/components/plan/PlanUpgradeDialog.vue'

export default {
  components: { LoanCard, LoanDialog, PlanUpgradeDialog },
  data () {
    return {
      showLoanDialog: false,
      maxBasicUserLoans: 3,
      showPlanUpgradeDialog: false
    }
  },
  computed: {
    loans () {
      return this.$store.getters['finances/getLoans']
    },
    numLoans () {
      return Object.keys(this.loans).length
    },
    isPremiumPlan () {
      return this.$store.getters['finances/getShowFullPlan']
    }
  },
  methods: {
    registerAddButtonClick () {
      if (this.isPremiumPlan || this.numLoans < this.maxBasicUserLoans) {
        this.showLoanDialog = true
      } else {
        this.showPlanUpgradeDialog = true
      }
    }
  }
}
</script>
