<template>
  <div>
    <v-row class="mb-4 ml-1">
      <v-btn
        fab
        large
        color="primary"
        @click.stop="showDialog=true"
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
  </div>
</template>

<script>
import GoalCard from '@/components/finances/GoalCard.vue'
import GoalDialog from '@/components/finances/GoalDialog.vue'

export default {
  components: { GoalCard, GoalDialog },
  data () {
    return {
      showDialog: false
    }
  },
  computed: {
    goals () {
      return this.$store.state.finances.user_finances.goals
    }
  }
}
</script>
