<template>
  <v-row>
    <v-col cols="12">
      <v-container class="my-n5">
        <v-card>
          <v-card-title>Net Worth at Retirement</v-card-title>
          <v-divider class="mb-1" />
          <v-container fluid>
            <div class="text-center text-h3 primary--text">
              {{ asDollar(finalNetWorth) }}
            </div>
          </v-container>
        </v-card>
      </v-container>
    </v-col>
    <v-col cols="12">
      <v-container class="my-n5">
        <v-card>
          <v-card-title>Priorities</v-card-title>
          <v-divider class="mb-1" />
          <v-container class="mb-2">
            <v-row v-for="(instrument, index) in instrumentPriorityOrder" :key="index" class="px-4 my-2">
              <div class="text">
                {{ index + 1 }}. {{ instrument }}
              </div>
            </v-row>
          </v-container>
        </v-card>
      </v-container>
    </v-col>
    <v-col cols="12">
      <v-container class="my-n5">
        <v-card>
          <v-card-title>Important Dates</v-card-title>
          <v-divider class="mb-1" />
          <v-container class="mb-2">
            <v-row v-for="(importantDate, index) in importantDates" :key="index" class="px-2 my-2">
              <div class="text">
                {{ importantDate.name }}
              </div>
              <v-spacer />
              <div class="text">
                {{ importantDate.date }}
              </div>
            </v-row>
          </v-container>
        </v-card>
      </v-container>
    </v-col>
  </v-row>
</template>

<script>
import { asDollar } from '~/assets/utils.js'

export default {
  props: ['selectedStrategy'],
  computed: {
    summaries () {
      // return this.summaryData[this.selectedStrategy].summaries
      return this.$store.getters['plan/getSummaries'](this.selectedStrategy)
    },
    finalNetWorth () {
      return this.summaries.net_worth
    },
    instrumentPriorityOrder () {
      return this.summaries.priorities
    },
    importantDates () {
      return this.summaries.important_dates
    }
  },
  methods: {
    asDollar
  }
}
</script>
