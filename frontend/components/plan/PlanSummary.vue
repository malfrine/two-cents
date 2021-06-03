<template>
  <v-row>
    <v-col cols="12">
      <v-container class="my-n5">
        <v-card>
          <TCTooltip :text="tooltips.netWorth" left>
            <template v-slot:inner>
              <v-card-title>
                Net Worth at Retirement
              </v-card-title>
            </template>
          </TCTooltip>
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
          <TCTooltip :text="tooltips.priorities" left>
            <template v-slot:inner>
              <v-card-title>
                Priorities
              </v-card-title>
            </template>
          </TCTooltip>
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
import TCTooltip from '@/components/base/TCTooltip.vue'
import { asDollar } from '~/assets/utils.js'

export default {
  components: {
    TCTooltip
  },
  props: ['selectedStrategy'],
  data () {
    return {
      tooltips: {
        plan: 'Select another plan type from this dropdown menu to see how it impacts your retirement net worth, debt-free date, and progress to your financial goals.',
        netWorth: 'This is an estimation of your net worth in retirement at this time. This number will change depending on how your financial goals and priorities change, how your income changes over your lifetime, and how you decide to save and spend your money. To get the most accurate estimation, update your information as regularly as you can!',
        priorities: "This shows the aspects of your financial picture that you should be focusing on growing (if it's a saving/investing account) or paying off (if it's a loan.)"
      }
    }
  },
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
