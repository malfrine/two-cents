import { makeFakePlan, RawPlanProcessor } from '~/assets/plan-utils.js'

const defaultState = function () {
  return {
    plan: null
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getStrategies (state) {
    return state.plan.strategies
  },
  getNetWorth (state) {
    return state.plan.net_worth
  },
  getSummary (state) {
    return state.plan.summary
  },
  getIsLoading (state) {
    return state.is_loading
  }
}

const mutations = {
  SET_PLAN (state, payload) {
    state.plan = payload
  }
}

const actions = {
  getPlan (context) {
    context.commit('SET_IS_LOADING', true)
    this.$axios.$get('/api/my/plan/processed')
      .then(
        (response) => {
          const rp = new RawPlanProcessor()
          rp.processResponse(response.data)
          context.commit('SET_PLAN', response.data)
          context.commit('SET_IS_LOADING', false)
        }
      )
      .catch(
        e => this.$toast.error('Uh oh, something went wrong')
      )
  },
  getFakePlan (context) {
    const data = makeFakePlan()
    const rp = new RawPlanProcessor()
    rp.processResponse(data)
    context.commit('SET_PLAN', data)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
