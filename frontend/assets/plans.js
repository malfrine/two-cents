
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
  constructor (instrumentColors) {
    this.instrumentColors = instrumentColors
  }

  fromResponseData (responseData) {
    const strategies = this.makeStrategies(responseData)
    const instruments = this.makeInstruments(responseData)
    const plans = this.makePlans(responseData)

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

  makePlans (responseData) {
    const plans = []
    for (const planName in responseData) {
      const planResponseData = responseData[planName]
      const netWorthForecastData = planResponseData.net_worth.datasets
      for (const index in netWorthForecastData) {
        const datum = netWorthForecastData[index]
        netWorthForecastData[index].backgroundColor = this.instrumentColors.getColor(datum.instrument_type, datum.instrument_id)
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

export { Plans }
