<template>
  <BaseExpandableObjectCard
    :name="goal.name"
    :summary-value="asDollar(goal.amount)"
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
import { asDollar } from '~/assets/utils.js'

export default {
  props: {
    goalId: {
      type: Number,
      required: true
    }
  },
  data () {
    return {
      showDialog: false
    }
  },
  computed: {
    goal () {
      return this.$store.getters['finances/getGoalById'](this.goalId)
    }
  },
  methods: {
    deleteGoal () {
      this.$store.dispatch('finances/deleteGoal', this.goal)
    },
    asDollar
  }
}
</script>
