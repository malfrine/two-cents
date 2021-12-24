
const initialState = function () {
  return {
    loggingIn: false,
    authUser: null,
    idToken: null
  }
}

const state = function () {
  return initialState()
}

const getters = {
  isLoggedIn: (state) => {
    try {
      return state.authUser.uid !== null
    } catch {
      return false
    }
  }
}

const mutations = {
  START_LOGIN (state) {
    state.loggingIn = true
  },
  STOP_LOGIN (state) {
    state.loggingIn = false
  },
  SET_AUTH_USER: (state, { authUser }) => {
    state.authUser = {
      uid: authUser.uid,
      email: authUser.email
    }
  },
  SET_ID_TOKEN: (state, { idToken }) => {
    state.idToken = idToken
  },
  RESET_STORE (state) {
    state.authUser = null
    state.loggingIn = false
    state.idToken = null
  }
}

const actions = {
  async nuxtServerInit ({ dispatch }, ctx) {
    // INFO -> Nuxt-fire Objects can be accessed in nuxtServerInit action via this.$fire___, ctx.$fire___ and ctx.app.$fire___'

    /** Get the VERIFIED authUser on the server */
    if (ctx.res && ctx.res.locals && ctx.res.locals.user) {
      const { allClaims: claims, ...authUser } = ctx.res.locals.user

      await dispatch('onAuthStateChanged', {
        authUser,
        claims
      })
    }
  },

  async onAuthStateChanged ({ commit }, { authUser }) {
    if (authUser && authUser.getIdToken) {
      try {
        const idToken = await authUser.getIdToken(true)
        commit('SET_ID_TOKEN', { idToken })
        commit('SET_AUTH_USER', { authUser })
      } catch (e) {
        this.$toast.error('Something went wrong with your login credentials')
        commit('RESET_STORE')
      }
    } else {
      commit('RESET_STORE')
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
