import Vue from 'vue'

const defaultState = function () {
  return {
    finances_updated_since_plan_built: true,
    user_finances: null,
    show_full_plan: false
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getFinancialProfile (state) {
    return state.user_finances?.financial_profile
  },
  getMonthlyAllowance (state) {
    return state.user_finances?.financial_profile?.monthly_allowance
  },
  getFirstName (state) {
    return state.user_finances?.first_name
  },
  getLoans (state) {
    return state.user_finances?.loans
  },
  getInvestments (state) {
    return state.user_finances?.investments
  },
  getLoanById: state => (id) => {
    return state.user_finances?.loans[id]
  },
  getInvestmentById: state => (id) => {
    return state.user_finances?.investments[id]
  },
  getUserFinancesExists (state) {
    return state.user_finances != null
  },
  getFinancesUpdateSinceLastPlanBuilt (state) {
    return state.finances_updated_since_plan_built
  },
  getGoals (state) {
    return state.user_finances?.goals
  },
  getGoalById: state => (id) => {
    return state.user_finances?.goals[id]
  }
}

const mutations = {
  SET_USER_FINANCES (state, payload) {
    state.user_finances = payload
    state.finances_updated_since_plan_built = true
  },
  RESET_USER_FINANCES (state) {
    Object.assign(state, defaultState())
    state.finances_updated_since_plan_built = true
  },
  SET_LOAN: (state, payload) => {
    Vue.set(state.user_finances.loans, payload.id, payload)
    state.finances_updated_since_plan_built = true
  },
  DELETE_LOAN: (state, payload) => {
    Vue.delete(state.user_finances.loans, payload.id)
    state.finances_updated_since_plan_built = true
  },
  SET_INVESTMENT: (state, payload) => {
    Vue.set(state.user_finances.investments, payload.id, payload)
    state.finances_updated_since_plan_built = true
  },
  DELETE_INVESTMENT: (state, payload) => {
    Vue.delete(state.user_finances.investments, payload.id)
    state.finances_updated_since_plan_built = true
  },
  SET_GOAL: (state, payload) => {
    Vue.set(state.user_finances.goals, payload.id, payload)
    state.finances_updated_since_plan_built = true
  },
  DELETE_GOAL: (state, payload) => {
    Vue.delete(state.user_finances.goals, payload.id)
    state.finances_updated_since_plan_built = true
  },
  SET_FINANCIAL_PROFILE: (state, payload) => {
    state.user_finances.financial_profile = payload
    state.finances_updated_since_plan_built = true
  },
  REGISTER_PLAN_UPDATED: (state) => {
    state.finances_updated_since_plan_built = false
  },
  SET_PAYMENT_PLAN: (state, payload) => {
    state.user_finances.payment_plan = payload
  }
}

const actions = {
  resetUserFinances (context) {
    context.commit('RESET_USER_FINANCES')
  },
  createOrUpdateLoan (context, payload) {
    if (payload.id == null) {
      this.$axios.$post('/api/my/finances/loans', payload)
        .then(
          (response) => {
            context.commit('SET_LOAN', response)
          }
        )
        .catch(
          (e) => {
            this.$sentry.captureException('Failed to create user loan', payload)
            this.$toast.error('Could not create loan')
          }
        )
    } else {
      this.$axios.$put(`/api/my/finances/loans/${payload.id}`, payload)
        .then(
          (response) => {
            context.commit('SET_LOAN', response)
          }
        )
        .catch(
          (e) => {
            this.$sentry.captureException('Failed to update user loan', payload)
            this.$toast.error('Could not update loan')
          }
        )
      this.$fire.analytics.logEvent('updated_finances')
    }
  },
  deleteLoan (context, payload) {
    this.$axios.$delete(`/api/my/finances/loans/${payload.id}`)
      .then(
        (response) => {
          context.commit('DELETE_LOAN', payload)
        }
      )
      .catch(
        (e) => {
          this.$sentry.captureException('Failed to delete user loan', payload)
          this.$toast.error('Could not delete loan')
        }
      )
    this.$fire.analytics.logEvent('updated_finances')
  },
  createOrUpdateInvestment (context, payload) {
    if (payload.id == null) {
      this.$axios.$post('/api/my/finances/investments', payload)
        .then(
          (response) => {
            context.commit('SET_INVESTMENT', response)
          }
        )
        .catch(
          (e) => {
            this.$sentry.captureException('Failed to add user investment', payload)
            this.$toast.error('Could not create investment')
          }
        )
    } else {
      this.$axios.$put(`/api/my/finances/investments/${payload.id}`, payload)
        .then(
          (response) => {
            context.commit('SET_INVESTMENT', response)
          }
        )
        .catch(
          (e) => {
            this.$sentry.captureException('Failed to update user investment', payload)
            this.$toast.error('Could not update investment')
          }
        )
      this.$fire.analytics.logEvent('updated_finances')
    }
  },
  deleteInvestment (context, payload) {
    this.$axios.$delete(`/api/my/finances/investments/${payload.id}`)
      .then(
        (response) => {
          context.commit('DELETE_INVESTMENT', payload)
        }
      )
      .catch(
        (e) => {
          this.$sentry.captureException('Failed to delete user investment', payload)
          this.$toast.error('Could not delete investment')
        }
      )
    this.$fire.analytics.logEvent('updated_finances')
  },
  createOrUpdateGoal (context, payload) {
    if (payload.id == null) {
      this.$axios.$post('/api/my/finances/goals', payload)
        .then(
          (response) => {
            context.commit('SET_GOAL', response)
          }
        )
        .catch(
          (e) => {
            this.$sentry.captureException('Failed to create user goal', payload)
            this.$toast.error('Could not create goal')
          }
        )
    } else {
      this.$axios.$put(`/api/my/finances/goals/${payload.id}`, payload)
        .then(
          (response) => {
            context.commit('SET_GOAL', response)
          }
        )
        .catch(
          (e) => {
            this.$sentry.captureException('Failed to update user goal', payload)
            this.$toast.error('Could not update goal')
          }
        )
      this.$fire.analytics.logEvent('updated_finances')
    }
  },
  deleteGoal (context, payload) {
    this.$axios.$delete(`/api/my/finances/goals/${payload.id}`)
      .then(
        (response) => {
          context.commit('DELETE_GOAL', payload)
        }
      )
      .catch(
        (e) => {
          this.$sentry.captureException('Failed to delete user goal', payload)
          this.$toast.error('Could not delete goal')
        }
      )
    this.$fire.analytics.logEvent('updated_finances')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
