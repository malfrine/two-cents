<template>
  <BaseDialog
    :visible="visible"
    title="Tell us about your goal"
    submit-text="Save Goal"
    @close="$emit('close')"
    @submit="createOrUpdateGoalAndClose()"
  >
    <template v-slot:form>
      <v-form ref="form">
        <v-tooltip v-model="show">
          <template v-slot:activator="{ on }">
            <v-text-field
              v-model="name"
              append-icon="mdi-information-outline"
              class="my-1"
              outlined
              label="Name"
              :rules="[v => !!v || 'Goal name is required']"
              @click:append="show = on;"
            />
          </template>
          <span>Goal name</span>
        </v-tooltip>
        <v-text-field
          v-model="name"
          class="my-1"
          outlined
          label="Name"
          :rules="[v => !!v || 'Goal name is required']"
        />
        <v-autocomplete
          v-model="type"
          label="Pick goal type"
          solo
          outlined
          item-color="primary"
          :items="goalTypes"
          :rules="[v => !!v || 'Goal type is required']"
        />
        <div v-show="showDetails">
          <v-divider class="mb-6" />
          <v-text-field
            v-model="amount"
            class="my-1"
            outlined
            label="Amount Needed"
            type="number"
            :rules="[v => !!v || 'Amount needed to complete goal is required']"
          />
          <v-text-field
            v-model="date"
            class="my-1"
            outlined
            label="Completion Date"
            type="date"
            :rules="[v => !!v || 'Completion date is required']"
          />
        </div>
      </v-form>
    </template>
  </BaseDialog>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    goalId: {
      type: Number,
      default: null
    }
  },

  data () {
    const goal = this.$store.getters['finances/getGoalById'](this.goalId) || {}
    return {
      id: goal.id,
      type: goal.type,
      name: goal.name,
      date: goal.date,
      amount: goal.amount,
      goalTypes: ['Nest Egg', 'Big Purchase'],
      show: false
    }
  },
  computed: {
    showDetails () {
      return this.type !== null & this.name !== null
    }
  },
  methods: {
    createOrUpdateGoalAndClose () {
      if (!this.$refs.form.validate()) {
        return
      }

      const goal = {
        id: this.id,
        type: this.type,
        name: this.name,
        date: this.date,
        amount: this.amount
      }

      this.$store.dispatch('finances/createOrUpdateGoal', goal)
      this.$emit('close')
    }
  }
}
</script>
