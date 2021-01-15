import { PlanMaker } from '~/assets/plans.js'

const defaultState = function () {
  return {
    plans: null
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getStrategies (state) {
    return state.plans.strategies || []
  },
  getNetWorth: state => (strategyName) => {
    return state.plans.data[strategyName].netWorthForecast
  },
  getSummary: state => (strategyName) => {
    return state.plans.data[strategyName].summary
  },
  getMilestones: state => (strategyName) => {
    return state.plans.data[strategyName].milestones
  }
}

const mutations = {
  SET_PLANS (state, payload) {
    console.log(payload)
    state.plans = payload
  }
}

const actions = {
  getPlan (context) {
    this.$axios.$get('/api/my/plan/processed')
      .then(
        (response) => {
          const plans = PlanMaker.fromResponseData(response.data)
          context.commit('SET_PLAN', plans)
        }
      )
      .catch(
        e => this.$toast.error('Uh oh, something went wrong')
      )
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
