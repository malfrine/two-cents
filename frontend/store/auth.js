
const state = function () {
  return {
    loggingIn: false,
    loggedIn: false
  } // only used to access private views
}

const getters = {}

const mutations = {
  START_LOGIN (state) {
    state.loggingIn = true
  },
  LOGIN (state) {
    state.loggingIn = false
    state.loggedIn = true
  },
  LOGOUT (state) {
    state.loggedIn = false
  },
  STOP_LOGIN (state) {
    state.loggingIn = false
  }
}

const actions = {
  postLogin (context, payload) {
    context.commit('START_LOGIN')
    return this.$axios.$post('/api/my/session', payload)
      .then((response) => {
        context.commit('LOGIN')
        this.$router.push('/dashboard/profile')
        context.comit('STOP_LOGIN')
      })
      .catch((e) => {
        if (e.response.status === 404) {
          this.$toast.error('Username or password is not recognized')
          context.commit('STOP_LOGIN')
        }
      })
  },
  postRegister (context, payload) {
    return this.$axios.$post('/api/my/account/', payload)
      .then((response) => {
        if (response.status === 210) {
          // Internal server error
          this.$toast.error('Sorry, could not register your account')
        } else {
          this.$router.push('/login')
        }
      })
      .catch((e) => { this.$toast.error('Sorry, could not register your account') })
  },
  postLogout (context, payload) {
    return this.$axios.$delete('/api/my/session')
      .then((response) => {
        context.commit('LOGOUT')
      })
      .catch((e) => { })
  },
  getLoginStatus (context, payload) {
    return this.$axios.$get('/api/my/session')
      .then((response) => {
        context.commit('LOGIN')
        this.$router.push('/dashboard/profile')
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
