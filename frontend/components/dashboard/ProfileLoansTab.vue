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
      <loan-card
        v-for="loan in loans"
        :key="loan.id"
        :loan-id="loan.id"
        :read-only="readOnly"
        :published-plan-id="publishedPlanId"
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
      showLoanDialog: false,
      maxBasicUserLoans: 3,
      showPlanUpgradeDialog: false
    }
  },
  computed: {
    loans () {
      if (this.publishedPlanId != null) {
        return this.$store.getters['published-plans/getLoans'](this.publishedPlanId)
      } else {
        return this.$store.getters['finances/getLoans']
      }
    },
    numLoans () {
      return Object.keys(this.loans).length
    },
    isPremiumPlan () {
      return this.$store.getters['users/getShowFullPlan']
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
