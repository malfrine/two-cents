const defaultState = function () {
  return {
    enums: {
      loan_types: [''],
      interest_types: ['']
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
  }
}

const mutations = {
  SET_ENUMS (state, payload) {
    state.enums = payload
  }
}

const actions = {
  getAllEnums (context) {
    console.log('getting all enums')
    return this.$axios.$get('/api/finances/enums') // TODO: change this to all enums down the line
      .then((response) => {
        console.log(response)
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
