import Vue from 'vue'

const defaultState = function () {
  return {
    is_loading: true,
    no_finances: true,
    user_finances: null
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getFinancialProfile (state) {
    return state.user_finances.financial_profile
  },
  getFirstName (state) {
    return state.user_finances.first_name
  },
  getLastName (state) {
    return state.user_finances.last_name
  },
  getEmail (state) {
    return state.user_finances.email
  },
  getLoans (state) {
    return state.user_finances.loans
  },
  getInvestments (state) {
    return state.user_finances.investments
  },
  getLoanById: state => (id) => {
    return state.user_finances.loans[id]
  },
  getInvestmentById: state => (id) => {
    return state.user_finances.investments[id]
  },
  getUserFinancesExists (state) {
    return state.user_finances != null
  }
}

const mutations = {
  SET_USER_FINANCES (state, payload) {
    state.user_finances = payload
    state.no_finances = false
  },
  RESET_USER_FINANCES (state) {
    Object.assign(state, defaultState())
  },
  SET_LOAN: (state, payload) => {
    Vue.set(state.user_finances.loans, payload.id, payload)
  },
  DELETE_LOAN: (state, payload) => {
    Vue.delete(state.user_finances.loans, payload.id)
  },
  SET_INVESTMENT: (state, payload) => {
    Vue.set(state.user_finances.investments, payload.id, payload)
  },
  DELETE_INVESTMENT: (state, payload) => {
    Vue.delete(state.user_finances.investments, payload.id)
  },
  SET_FINANCIAL_PROFILE: (state, payload) => {
    state.user_finances.financial_profile = payload
  },
  SET_IS_LOADING: (state, payload) => {
    state.is_loading = payload
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
            this.$toast.error('Could not update loan')
          }
        )
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
          this.$toast.error('Could not delete loan')
        }
      )
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
            this.$toast.error('Could not update investment')
          }
        )
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
          this.$toast.error('Could not delete investment')
        }
      )
  },
  updateFinancialProfile (context, payload) {
    this.$axios.$post('/api/my/finances/profile', payload)
      .then(
        (response) => {
          context.commit('SET_FINANCIAL_PROFILE', response)
        }
      )
      .catch(
        (e) => { this.$toast.error('Could not update your information') }
      )
  },
  setIsLoading (context, payload) {
    context.commit('SET_IS_LOADING', payload)
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
