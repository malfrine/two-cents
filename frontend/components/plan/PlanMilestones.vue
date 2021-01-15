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
          v-text="m.date.toDateString()"
        />
      </template>
      <v-card elevation="2">
        <v-card-text class="headline">
          {{ m.header }}
          <v-divider v-if="!$vuetify.breakpoint.smAndUp" class="my-3" />
          <span
            v-if="!$vuetify.breakpoint.smAndUp"
            class="headline font-weight-bold"
            v-text="m.date.toDateString()"
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
  props: ['selectedStrategy'],
  computed: {
    milestones () {
      return this.$store.getters['plan/getMilestones'](this.selectedStrategy)
    }
  },
  methods: {
    getHeader (m) {
      return this.$vuetify.breakpoint.smAndUp ? m.header : `${m.date.toDateString()} - ${m.header}`
    }
  }
}
</script>
