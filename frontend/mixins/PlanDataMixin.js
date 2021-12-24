export default {
  data () {
    return {
      selectedStrategy: 'Investment-Focused Plan',
      tooltips: {
        netWorthProjection: 'This graph shows how your net worth will change up to retirement. To view your finances at a single point in time, move your cursor until you have reached your desired date. The legend at the top of the graph indicates the different elements of your financial picture.',
        currentFinances: "This section of your plan shows your loans and investments. These values can be updated by visiting the 'Profile' tab on the left side of the screen.",
        milestones: 'Keep track of your milestones and financial goals with this timeline. Each milestone contains important information about each event such as interest paid and the time it took to achieve the milestone.',
        actionPlan: 'This is your payment plan for the next 3 months as caculated by our algorithm. This payment plan is made in consideration of a variety of factors including: principal balances of your loans, interest rates of your loans, term lengths, financial goals, investment types, investment risk tolerance, and monthly allowance (to name a few.)',
        strategies: 'Select another plan type from this dropdown menu to see how it impacts your retirement net worth, debt-free date, and progress to your financial goals.'
      }
    }
  },
  computed: {

    netWorthData () {
      let refData
      if (this.isPublishedPlan) {
        refData = this.$store.getters['published-plans/getNetWorth'](this.publishedPlanId, this.selectedStrategy)
      } else {
        refData = this.$store.getters['plan/getNetWorth'](this.selectedStrategy)
      }
      return JSON.parse(JSON.stringify(refData))
    },
    strategies () {
      if (this.isPublishedPlan) {
        return this.$store.getters['published-plans/getStrategies'](this.publishedPlanId)
      } else {
        return this.$store.getters['plan/getStrategies']
      }
    },
    possessiveUserName () {
      if (this.isPublishedPlan) {
        return 'Your Potential'
      } else {
        const firstName = this.$store.getters['users/getFirstName']
        if (!firstName) {
          return 'Your '
        }
        const posession = firstName.slice(-1) === 's' ? "'" : "'s"
        return `${firstName}${posession}`
      }
    },

    chartHeight () {
      switch (this.$vuetify.breakpoint.name) {
        case 'xs': return 300
        case 'sm': return 400
        case 'md': return 400
        case 'lg': return 600
        case 'xl': return 700
      }
      return 800
    },
    chartStyles () {
      return {
        position: 'relative',
        height: `${this.chartHeight}px`
      }
    }
  }
}
