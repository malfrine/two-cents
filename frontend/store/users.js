const defaultState = function () {
  return {
    user: {
      first_name: '',
      last_name: '',
      email: '',
      payment_plan: {},
      is_admin: false,
      is_staff: false,
      is_active: false
    }
  }
}

const state = function () {
  return defaultState()
}

const getters = {
  getFirstName (state) {
    return state.user?.first_name
  },
  getLastName (state) {
    return state.user?.last_name
  },
  getEmail (state) {
    return state.user?.email
  },
  getUserInfoExists (state) {
    return state.user != null
  },
  getShowFullPlan (state) {
    if (!state.user.payment_plan?.is_premium_plan) {
      return false
    }
    const dateString = state.user.payment_plan?.expiration_dt
    if (dateString) {
      return new Date(dateString) >= new Date()
    }
    return false
  },
  getIsPremiumPlan (state) {
    return state.user.payment_plan?.is_premium_plan
  },
  getIsSubscriptionPlan (state) {
    return state.user.payment_plan?.is_subscription_plan
  },
  getPlanType (state) {
    return state.user.payment_plan?.plan_type
  },
  getIsCancelledPlan (state) {
    return state.user.payment_plan?.is_cancelled
  },
  getVerbosePlanType (state) {
    return state.user.payment_plan?.verbose_plan_type
  },
  getIsAdminUser (state) {
    return state.user.is_admin && state.user.is_active && state.user.is_staff
  }
}

const mutations = {
  SET_USER_INFO (state, payload) {
    state.user = payload
  },
  RESET_USER_INFO (state) {
    Object.assign(state, defaultState())
  },
  SET_PAYMENT_PLAN: (state, payload) => {
    state.user.payment_plan = payload
  }
}

const actions = {
  resetUserInfo (context) {
    context.commit('RESET_USER_INFO')
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
