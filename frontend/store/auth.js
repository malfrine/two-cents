
const state = function () {
  return {
    loggingIn: false,
    loggedIn: false
  } // only used to access private views
}

const getters = {}

const mutations = {
  startLogin (state) {
    state.loggingIn = true
  },
  login (state) {
    state.loggingIn = false
    state.loggedIn = true
  },
  logout (state) {
    state.loggedIn = false
  }
}

const actions = {
  postLogin (context, payload) {
    console.log(this.$store)
    context.commit('startLogin')
    return this.$axios.$post('/api/users/login/', payload)
      .then((response) => {
        context.commit('login')
        this.$router.push('/dashboard/profile')
      })
      .catch((e) => {
        console.log(e)
      })
  },
  postRegister (context, payload) {
    return this.$axios.$post('/api/users/register/', payload)
      .then((response) => {
        console.log(response)
        if (response.status === 210) {
          // Internal server error
          console.log(response)
        } else {
          this.$router.push('/login')
        }
      })
      .catch((e) => { console.log(e) })
  },
  postLogout (context, payload) {
    return this.$axios.$post('/api/users/logout/')
      .then((response) => {
        context.commit('logout')
      })
      .catch((e) => { console.log(e) })
  },
  getLoginStatus (context, payload) {
    return this.$axios.$get('/api/users/check_login')
      .then((response) => {
        context.commit('login')
        this.$router.push('/dashboard/profile')
      })
      .catch((e) => { console.log(e) })
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
