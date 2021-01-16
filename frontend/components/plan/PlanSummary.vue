<template>
  <v-row>
    <v-container>
      <v-col v-for="summary in testSummaries" :key="summary.name" cols="12">
        <v-card>
          <v-card-title>
            {{ summary.name }}
          </v-card-title>
          <v-divider class="my-1" />
          <v-card-subtitle>
            {{ summary.text }}
          </v-card-subtitle>
        </v-card>
      </v-col>
    </v-container>
  </v-row>
</template>

<script>
export default {
  props: ['selectedStrategy'],
  data () {
    return {
      summaries: {
        'summary 1': {
          name: 'Priorities',
          text: 'This is a summary of your priorities'
        },
        'summary 2': {
          name: 'Important Dates',
          text: 'This is a summary of your important dates'
        },
        'summary 3': {
          name: 'Money Saved',
          text: 'This is a summary of how much money you can save'
        }
      }
    }
  },
  computed: {
    testSummaries () {
      return this.$store.getters['plan/getSummaries'](this.selectedStrategy)
    }
  }
}
</script>
