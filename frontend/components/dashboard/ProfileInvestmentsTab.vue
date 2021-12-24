<template>
  <div>
    <v-row v-if="!readOnly" class="mb-4 ml-1">
      <v-btn
        fab
        large
        color="primary"
        :disabled="readOnly"
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
        :read-only="readOnly"
        :published-plan-id="publishedPlanId"
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
  props: {
    readOnly: {
      type: Boolean,
      default: false
    },
    publishedPlanId: {
      type: Number,
      default: null
    }
  },
  data () {
    return {
      showInvestmentDialog: false,
      maxBasicUserInvestments: 4,
      showPlanUpgradeDialog: false
    }
  },
  computed: {
    investments () {
      if (this.publishedPlanId != null) {
        return this.$store.getters['published-plans/getInvestments'](this.publishedPlanId) || {}
      } else {
        return this.$store.getters['finances/getInvestments'] || {}
      }
    },
    numInvestments () {
      return Object.keys(this.investments).length
    },
    isPremiumPlan () {
      return this.$store.getters['users/getShowFullPlan']
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
