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
      <investment-card
        v-for="investment in investments"
        :key="investment.id"
        :investment-id="investment.id"
      />
    </v-row>
    <InvestmentDialog :visible="showInvestmentDialog" :investment-id="null" @close="showInvestmentDialog=false" />
    <PlanUpgradeDialog
      :visible="showPlanUpgradeDialog"
      @close="showPlanUpgradeDialog=false"
      @payment-made="showPlanUpgradeDialog=false"
    />
  </div>
</template>

<script>
import InvestmentCard from '@/components/finances/InvestmentCard.vue'
import InvestmentDialog from '@/components/finances/InvestmentDialog.vue'
import PlanUpgradeDialog from '@/components/plan/PlanUpgradeDialog.vue'

export default {
  components: { InvestmentCard, InvestmentDialog, PlanUpgradeDialog },
  data () {
    return {
      showInvestmentDialog: false,
      maxBasicUserInvestments: 4,
      showPlanUpgradeDialog: false
    }
  },
  computed: {
    investments () {
      return this.$store.getters['finances/getInvestments']
    },
    numInvestments () {
      return Object.keys(this.investments).length
    },
    isPremiumPlan () {
      return this.$store.getters['finances/getShowFullPlan']
    }
  },
  methods: {
    registerAddButtonClick () {
      if (this.isPremiumPlan || this.numInvestments < this.maxBasicUserInvestments) {
        this.showInvestmentDialog = true
      } else {
        this.showPlanUpgradeDialog = true
      }
    }
  }
}
</script>
