
const state = function () {
  return {
    referralCode: null
  }
}

const getters = {}

const mutations = {
  SET_REFERRAL_CODE (state, payload) {
    state.referralCode = payload
  }
}

const actions = {
  setReferralCode (context, payload) {
    context.commit('SET_REFERRAL_CODE', payload)
  }
}

export { state, getters, mutations, actions }
