import Vue from 'vue'

import { PlanMaker } from '~/assets/plans.js'

const defaultState = function () {
  return {
    published: {}
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getPublishedPlanExists: state => (planId) => {
    return state.published[planId] != null
  },
  getFinancialProfile: state => (planId) => {
    return state.published[planId]?.financial_data?.financial_profile
  },
  getMonthlyAllowance: state => (planId) => {
    return state.published[planId]?.financial_data?.financial_profile?.monthly_allowance
  },
  getLoans: state => (planId) => {
    return state.published[planId]?.financial_data?.loans
  },
  getInvestments: state => (planId) => {
    return state.published[planId]?.financial_data?.investments
  },
  getLoanById: state => (planId, loanId) => {
    return state.published[planId]?.financial_data?.loans[loanId]
  },
  getInvestmentById: state => (planId, investmentId) => {
    return state.published[planId]?.financial_data?.investments[investmentId]
  },
  getUserFinancesExists: state => (planId) => {
    return state.published[planId].financial_data != null
  },
  getGoals: state => (planId) => {
    return state.published[planId]?.financial_data?.goals
  },
  getGoalById: state => (planId, goalId) => {
    return state.published[planId]?.financial_data?.goals[goalId]
  },
  getPlans: state => (planId) => {
    return state.published[planId].plans
  },
  getStrategies: state => (planId) => {
    return state.published[planId].plans.strategies
  },
  getNetWorth: state => (planId, strategyName) => {
    return state.published[planId].plans.data[strategyName].netWorthForecast
  },
  getSummaries: state => (planId, strategyName) => {
    return state.published[planId].plans.data[strategyName].summaries
  },
  getActionPlan: state => (planId, strategyName) => {
    return state.published[planId].plans.data[strategyName].actionPlan
  },
  getMilestones: state => (planId, strategyName) => {
    return state.published[planId].plans.data[strategyName].milestones
  },
  getIsPlansAvailable: state => (planId) => {
    return state.published[planId].plans != null
  }
}

const mutations = {
  SET_PLAN (state, payload) {
    Vue.set(state.published, payload.id, payload)
  }
}

const actions = {
  getPlanIfNotExists (context, payload) {
    const planId = payload.id
    const planExists = context.getters.getPublishedPlanExists(planId)
    if (planExists) {
      return null
    }
    this.$axios.get(`/api/published-plan/${planId}`)
      .then((response) => {
        const pm = new PlanMaker(this.$instrument.colors)
        const plans = pm.fromResponseData(response.data.plans)
        const payload = {
          plans,
          id: response.data.id,
          financial_data: response.data.financial_data
        }
        context.commit('SET_PLAN', payload)
      })
      .catch((e) => {
        return null
      })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
