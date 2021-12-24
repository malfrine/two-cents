<template>
  <BaseExpandableObjectCard
    :name="goal.name"
    :summary-value="asDollar(goal.amount)"
    :icon="$instrument.icons.getIcon(goal.type)"
    :read-only="readOnly"
    @open-dialog="showDialog = true"
    @delete-object="deleteGoal()"
  >
    <template v-slot:dialog>
      <GoalDialog :visible="showDialog" :goal-id="goal.id" @close="showDialog=false" />
    </template>
    <template v-slot:hidden>
      <v-card-text>
        <p class="mt-n3">
          <em> Goal Type: </em> {{ goal.type }}
        </p>
        <p class="mt-n3">
          <em> Due Date: </em> {{ goal.date }}
        </p>
      </v-card-text>
    </template>
  </BaseExpandableObjectCard>
</template>

<script>
import GoalDialog from '@/components/finances/GoalDialog'
import { asDollar } from '~/assets/utils.js'

export default {
  components: {
    GoalDialog
  },
  props: {
    goalId: {
      type: Number,
      required: true
    },
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
      showDialog: false
    }
  },
  computed: {
    goal () {
      if (this.publishedPlanId != null) {
        return this.$store.getters['published-plans/getGoalById'](this.publishedPlanId, this.goalId)
      } else {
        return this.$store.getters['finances/getGoalById'](this.goalId)
      }
    }
  },
  methods: {
    deleteGoal () {
      if (this.isPublishedPlan) {
        return null
      }
      this.$store.dispatch('finances/deleteGoal', this.goal)
    },
    asDollar
  }
}
</script>
