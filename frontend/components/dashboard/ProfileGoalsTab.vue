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
      <GoalCard
        v-for="goal in $store.state.finances.user_finances.goals"
        :key="goal.id"
        :goal-id="goal.id"
      />
    </v-row>
    <GoalDialog :visible="showDialog" @close="showDialog=false" />
    <PlanUpgradeDialog
      :visible="showPlanUpgradeDialog"
      @close="showPlanUpgradeDialog=false"
      @payment-made="showPlanUpgradeDialog=false"
    />
  </div>
</template>

<script>
import GoalCard from '@/components/finances/GoalCard.vue'
import GoalDialog from '@/components/finances/GoalDialog.vue'
import PlanUpgradeDialog from '@/components/plan/PlanUpgradeDialog.vue'

export default {
  components: { GoalCard, GoalDialog, PlanUpgradeDialog },
  data () {
    return {
      showDialog: false,
      maxBasicUserGoals: 3,
      showPlanUpgradeDialog: false
    }
  },
  computed: {
    goals () {
      return this.$store.state.finances.user_finances.goals
    },
    numGoals () {
      return Object.keys(this.goals).length
    },
    premiumPlan () {
      return this.$store.getters['finances/getShowFullPlan']
    }
  },
  methods: {
    registerAddButtonClick () {
      if (this.premiumPlan || this.numGoals < this.maxBasicUserGoals) {
        this.showDialog = true
      } else {
        this.showPlanUpgradeDialog = true
      }
    }
  }
}
</script>
