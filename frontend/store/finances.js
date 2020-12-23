import Vue from 'vue'

const state = function () {
  return {
    is_loading: true,
    no_finances: true,
    user_finances: {
      first_name: '',
      last_name: '',
      email: '',
      loans: {},
      investments: {},
      financial_profile: {}
    }
  }
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
  }
}

const mutations = {
  setUserFinances (state, payload) {
    state.user_finances = payload
    state.no_finances = false
    console.log(state.no_finances)
  },
  setLoan: (state, payload) => {
    Vue.set(state.user_finances.loans, payload.id, payload)
  },
  deleteLoan: (state, payload) => {
    console.log(payload)
    Vue.delete(state.user_finances.loans, payload.id)
  },
  setInvestment: (state, payload) => {
    Vue.set(state.user_finances.investments, payload.id, payload)
  },
  deleteInvestment: (state, payload) => {
    Vue.delete(state.user_finances.investments, payload.id)
  },
  setFinancialProfile: (state, payload) => {
    Vue.set(state.user_finances.financial_profile, payload)
  },
  setIsLoading: (state, payload) => {
    state.is_loading = payload
  }
}

const actions = {
  getUserFinances (context, payload) {
    return this.$axios.$get('/api/my/finances')
      .then((response) => {
        if (response.financial_profile == null) {
          response.financial_profile = {}
          // TODO: do this in a cleaner way
        }
        context.commit('setUserFinances', response)
        context.commit('setIsLoading', false)
      })
      .catch((e) => {
        console.log(e)
      })
  },
  createOrUpdateLoan (context, payload) {
    console.log(payload)
    if (payload.id == null) {
      this.$axios.$post('/api/my/finances/loans', payload)
        .then(
          (response) => {
            context.commit('setLoan', response)
          }
        )
        .catch(
          (e) => {
            console.log(e)
          }
        )
    } else {
      this.$axios.$put(`/api/my/finances/loans/${payload.id}`, payload)
        .then(
          (response) => {
            context.commit('setLoan', response)
          }
        )
        .catch(
          (e) => {
            console.log(e)
          }
        )
    }
  },
  deleteLoan (context, payload) {
    this.$axios.$delete(`/api/my/finances/loans/${payload.id}`)
      .then(
        (response) => {
          context.commit('deleteLoan', payload)
        }
      )
      .catch(
        (e) => {
          console.log(e)
        }
      )
  },
  createOrUpdateInvestment (context, payload) {
    if (payload.id == null) {
      this.$axios.$post('/api/my/finances/investments', payload)
        .then(
          (response) => {
            context.commit('setInvestment', response)
          }
        )
        .catch(
          (e) => {
            console.log(e)
          }
        )
    } else {
      this.$axios.$put(`/api/my/finances/investments/${payload.id}`, payload)
        .then(
          (response) => {
            context.commit('setInvestment', response)
          }
        )
        .catch(
          (e) => {
            console.log(e)
          }
        )
    }
  },
  deleteInvestment (context, payload) {
    this.$axios.$delete(`/api/my/finances/investments/${payload.id}`)
      .then(
        (response) => {
          context.commit('deleteInvestment', payload)
        }
      )
      .catch(
        (e) => {
          console.log(e)
        }
      )
  },
  updateFinancialProfile (context, payload) {
    this.$axios.$post('/api/my/finances/profile', payload)
      .then(
        (response) => {
          context.commit('setFinancialProfile', response)
        }
      )
      .catch(
        e => console.log(e)
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
