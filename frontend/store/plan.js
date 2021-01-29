
const defaultState = function () {
  return {
    plans: null
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getPlans (state) {
    return state.plans
  },
  getStrategies (state) {
    return state.plans.strategies
  },
  getNetWorth: state => (strategyName) => {
    return state.plans.data[strategyName].netWorthForecast
  },
  getSummaries: state => (strategyName) => {
    return state.plans.data[strategyName].summaries
  },
  getActionPlan: state => (strategyName) => {
    return state.plans.data[strategyName].actionPlan
  },
  getMilestones: state => (strategyName) => {
    return state.plans.data[strategyName].milestones
  }
}

const mutations = {
  SET_PLANS (state, payload) {
    state.plans = payload
  },
  RESET_PLANS (state) {
    state.plans = defaultState()
  }
}

const actions = {
  resetPlans (context) {
    context.commit('RESET_PLANS')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
