<template>
  <v-timeline :dense="!$vuetify.breakpoint.smAndUp">
    <v-timeline-item
      v-for="(m, title) in milestones"
      :key="title"
      color="primary"
    >
      <template v-slot:opposite>
        <span
          class="headline font-weight-bold"
          v-text="new Date(m.date).toDateString()"
        />
      </template>
      <v-card elevation="2">
        <v-card-text class="headline">
          <div :style="`color: ${getColor(m)}`">
            {{ m.header }}
          </div>
          <v-divider v-if="!$vuetify.breakpoint.smAndUp" class="my-3" />
          <span
            v-if="!$vuetify.breakpoint.smAndUp"
            class="headline font-weight-bold"
            v-text=" new Date(m.date).toDateString()"
          />
        </v-card-text>
        <v-card-text class="mt-n3">
          {{ m.text }}
        </v-card-text>
      </v-card>
    </v-timeline-item>
  </v-timeline>
</template>

<script>
export default {
  props: {
    selectedStrategy: {
      type: String,
      required: true
    },
    publishedPlanId: {
      type: Number,
      default: null
    }
  },
  computed: {
    milestones () {
      if (this.publishedPlanId != null) {
        return this.$store.getters['published-plans/getMilestones'](this.publishedPlanId, this.selectedStrategy)
      } else {
        return this.$store.getters['plan/getMilestones'](this.selectedStrategy)
      }
    }
  },
  methods: {
    getHeader (m) {
      return this.$vuetify.breakpoint.smAndUp ? m.header : `${new Date(m.date).toDateString()} - ${m.header}`
    },
    getColor (milestone) {
      const instrumentId = milestone.instrument_id
      const instrumentType = milestone.instrument_type
      if (instrumentId & instrumentId) {
        return this.$instrument.colors.getColor(instrumentType, instrumentId)
      }
    }
  }
}
</script>
