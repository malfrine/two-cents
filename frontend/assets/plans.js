import { ColorGetter } from './colors.js'

const makeFakePlansResponseData = function () {
  return {
    'Two Cents Plan': {
      net_worth: {
        datasets: [
          {
            label: 'Loan 1',
            data: [-12, -19, -3, 0]
          },
          {
            label: 'Loan 2',
            data: [-40, -30, -20, 0]
          },
          {
            label: 'Investment 2',
            data: [0, 20, 30, 40]
          },
          {
            label: 'Investment 3',
            data: [0, 20, 30, 40]
          }
        ],
        labels: [new Date('January 1, 2020'), new Date('February 1, 2020'), new Date('March 1, 2020'), new Date('April 1, 2020')]
      },
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
      },
      milestones: {
        'Milestone # 1 TC': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 2 TC': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 3 TC': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        }
      },
      action_plan: {
        monthly_allowance: 500,
        payments: {
          'loan 1': {
            instrument: 'loan 1',
            payment: 100
          },
          'loan 2': {
            instrument: 'loan 2',
            payment: 300
          },
          'investment 1': {
            instrument: 'investment 1',
            payment: 0
          },
          'investment 2': {
            instrument: 'investment 2',
            payment: 100
          }
        }
      }
    },
    'Avalanche Plan': {
      net_worth: {
        datasets: [
          {
            label: 'Loan 1',
            data: [-12, -19, -3, 0]
          },
          {
            label: 'Loan 2',
            data: [-40, -30, -20, 0]
          }
        ],
        labels: [new Date('January 1, 2020'), new Date('February 1, 2020'), new Date('March 1, 2020'), new Date('April 1, 2020')]

      },
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
      },
      milestones: {
        'Milestone # 1 AV': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 2 AV': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 3 AV': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        }
      },
      action_plan: {
        monthly_allowance: 500,
        payments: {
          'loan 1': {
            instrument: 'loan 1',
            payment: 100
          },
          'loan 2': {
            instrument: 'loan 2',
            payment: 300
          },
          'investment 1': {
            instrument: 'investment 1',
            payment: 0
          },
          'investment 2': {
            instrument: 'investment 2',
            payment: 100
          }
        }
      }
    },
    'Snowball Plan': {
      net_worth: {
        datasets: [
          {
            label: 'Loan 1',
            data: [-12, -19, -3, 0]
          },
          {
            label: 'Loan 2',
            data: [-40, -30, -20, 0]
          }
        ],
        labels: [new Date('January 1, 2020'), new Date('February 1, 2020'), new Date('March 1, 2020'), new Date('April 1, 2020')]

      },
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
      },
      milestones: {
        'Milestone # 1 SB': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 2 SB': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 3 SB': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        }
      },
      action_plan: {
        monthly_allowance: 500,
        payments: {
          'loan 1': {
            instrument: 'loan 1',
            payment: 100
          },
          'loan 2': {
            instrument: 'loan 2',
            payment: 300
          },
          'investment 1': {
            instrument: 'investment 1',
            payment: 0
          },
          'investment 2': {
            instrument: 'investment 2',
            payment: 100
          }
        }
      }
    },
    'Constant Payments Plan': {
      net_worth: {
        datasets: [
          {
            label: 'Loan 1',
            data: [-12, -19, -3, 0]
          },
          {
            label: 'Loan 2',
            data: [-40, -30, -20, 0]
          }
        ],
        labels: [new Date('January 1, 2020'), new Date('February 1, 2020'), new Date('March 1, 2020'), new Date('April 1, 2020')]

      },
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
      },
      milestones: {
        'Milestone # 1 CPP': {
          date: new Date(),
          header: 'Paid of Loan 1',
          text: 'Paid off Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 2 CPP': {
          date: new Date(),
          header: 'Paid of Loan 1',
          text: 'Paid off Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 3 CPP': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        },
        'Milestone # 4 CPP': {
          date: new Date(),
          header: 'Paid off Loan 1',
          text: 'Paid of Loan 1 20 days before schedule. Paid $20 on interest'
        }
      },
      action_plan: {
        monthly_allowance: 500,
        payments: {
          'loan 1': {
            instrument: 'loan 1',
            payment: 100
          },
          'loan 2': {
            instrument: 'loan 2',
            payment: 300
          },
          'investment 1': {
            instrument: 'investment 1',
            payment: 0
          },
          'investment 2': {
            instrument: 'investment 2',
            payment: 100
          }
        }
      }
    }
  }
}

class Plans {
    data = null
    strategies = null
    instruments = null

    constructor (plans, strategies, instruments) {
      const data = {}
      for (const planIndex in plans) {
        data[plans[planIndex].name] = plans[planIndex]
      }
      this.data = data
      this.strategies = strategies
      this.instruments = instruments
    }
}

class Plan {
    netWorthForecast = null
    summaries = null
    milestones = null
    actionPlan = null
    name = null

    constructor (netWorthForecast, summaries, milestones, actionPlan, name) {
      this.netWorthForecast = netWorthForecast
      this.summaries = summaries
      this.milestones = milestones
      this.actionPlan = actionPlan
      this.name = name
    }
}

export class PlanMaker {
    colorGetter = null

    constructor () {
      this.colorGetter = new ColorGetter()
    }

    fromResponseData (responseData) {
      const strategies = this.makeStrategies(responseData)
      const instruments = this.makeInstruments(responseData)
      const plans = this.makePlans(responseData, instruments)

      return new Plans(plans, strategies, instruments)
    }

    makeStrategies (responseData) {
      return Object.keys(responseData)
    }

    makeInstruments (responseData) {
      const instruments = new Set()
      for (const planName in responseData) {
        for (const index in responseData[planName].net_worth.datasets) {
          instruments.add(responseData[planName].net_worth.datasets[index].label)
        }
      }
      return Array.from(instruments)
    }

    makePlans (responseData, instruments) {
      const instrumentColorMap = {}
      for (const index in instruments) {
        instrumentColorMap[instruments[index]] = this.colorGetter.getNextColor()
      }
      const plans = []
      for (const planName in responseData) {
        const planResponseData = responseData[planName]
        const netWorthForecastData = planResponseData.net_worth.datasets
        for (const index in netWorthForecastData) {
          netWorthForecastData[index].backgroundColor = instrumentColorMap[netWorthForecastData[index].label]
        }
        const plan = new Plan(
          planResponseData.net_worth,
          planResponseData.summaries,
          planResponseData.milestones,
          planResponseData.action_plan,
          planName
        )
        plans.push(plan)
      }
      return plans
    }
}

export { makeFakePlansResponseData, Plans }
