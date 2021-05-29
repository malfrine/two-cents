
const state = function () {
  return {
    referralCode: null,
    referreeCode: null
  }
}

const getters = {}

const mutations = {
  SET_REFERRAL_CODE (state, payload) {
    state.referralCode = payload
  },
  SET_REFERREE_CODE (state, payload) {
    state.referreeCode = payload
  }
}

const actions = {
  setReferralCode (context, payload) {
    context.commit('SET_REFERRAL_CODE', payload)
  }
}

export { state, getters, mutations, actions }
