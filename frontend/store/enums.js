const defaultState = function () {
  return {
    exists: false,
    enums: {
      loan_types: [''],
      interest_types: [''],
      investment_fields: {},
      risk_levels: [''],
      volatility_choices: [''],
      provinces: [''],
      loan_fields: {}
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
    return Object.keys(state.enums.loan_fields)
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
  getRequiredLoanFields: state => (loanType, interestType) => {
    const mandatoryFields = state.enums.loan_fields[loanType] || []
    const interestField = state.enums.loan_interest_types_fields[interestType] || ''
    return [...mandatoryFields, interestField]
  },
  getStateExists (state) {
    return state.exists
  },
  getProvinces (state) {
    return state.enums.provinces
  },
  getInvestmentAccountTypes (state) {
    return state.enums.investment_account_types
  }
}

const mutations = {
  SET_ENUMS (state, payload) {
    state.enums = payload
    state.exists = true
  }
}

const actions = {
  getAllEnumsIfNeeded (context) {
    if (context.getters.getStateExists) {
      return
    }
    return this.$axios.$get('/api/finances/enums') // TODO: change this to all enums down the line
      .then((response) => {
        context.commit('SET_ENUMS', response)
      })
      .catch((e) => {
        this.$sentry.captureException('Unable to get enums', e)
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
