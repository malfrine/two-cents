const defaultState = function () {
  return {
    exists: false,
    enums: {
      loan_types: [''],
      interest_types: [''],
      investment_fields: {},
      risk_levels: [''],
      volatility_choices: ['']
    }
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getInterestTypes (state) {
    return state.enums.interest_types
  },
  getLoanTypes (state) {
    return Object.keys(state.enums.loan_types)
  },
  isRevolving: state => (loanType) => {
    const loanBehaviour = state.enums.loan_types[loanType] || ''
    return loanBehaviour.toUpperCase() === 'REVOLVING'
  },
  getInvestmentTypes (state) {
    return Object.keys(state.enums.investment_fields)
  },
  getRiskLevels (state) {
    return state.enums.risk_levels
  },
  getVolatilityChoices (state) {
    return state.enums.volatility_choices
  },
  getRequiredFields: state => (investmentType) => {
    return state.enums.investment_fields[investmentType] || []
  },
  getStateExists (state) {
    return state.exists
  }
}

const mutations = {
  SET_ENUMS (state, payload) {
    state.enums = payload
    state.exists = true
  }
}

const actions = {
  getAllEnums (context) {
    if (context.getters.getStateExists) {
      return
    }
    return this.$axios.$get('/api/finances/enums') // TODO: change this to all enums down the line
      .then((response) => {
        context.commit('SET_ENUMS', response)
      })
      .catch((e) => { })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
