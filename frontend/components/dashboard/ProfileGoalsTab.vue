<template>
  <div>
    <v-row v-if="!readOnly" class="mb-4 ml-1">
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
        v-for="goal in goals"
        :key="goal.id"
        :goal-id="goal.id"
        :read-only="readOnly"
        :published-plan-id="publishedPlanId"
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
  props: {
    readOnly: {
      type: Boolean,
      default: true
    },
    publishedPlanId: {
      type: Number,
      default: null
    }
  },
  data () {
    return {
      showDialog: false,
      maxBasicUserGoals: 3,
      showPlanUpgradeDialog: false
    }
  },
  computed: {
    goals () {
      if (this.publishedPlanId != null) {
        return this.$store.getters['published-plans/getGoals'](this.publishedPlanId) || {}
      } else {
        return this.$store.getters['finances/getGoals'] || {}
      }
    },
    numGoals () {
      return Object.keys(this.goals).length
    },
    premiumPlan () {
      return this.$store.getters['users/getShowFullPlan']
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
