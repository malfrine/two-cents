
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
  },
  stopLogin (state) {
    state.loggingIn = false
  }
}

const actions = {
  postLogin (context, payload) {
    context.commit('startLogin')
    return this.$axios.$post('/api/my/session', payload)
      .then((response) => {
        context.commit('login')
        this.$router.push('/dashboard/profile')
      })
      .catch((e) => {
        if (e.response.status === 404) {
          // send alert
          this.$toast.error('Username or password is not recognized', {
            duration: 3000,
            action: {
              icon: 'check',
              onClick: (e, toast) => {
                toast.goAway(0)
              }
            }
          })
          console.log(this.$toast)
          console.log("I don't know you")
          context.commit('stopLogin')
        }
      })
  },
  postRegister (context, payload) {
    console.log(payload)
    return this.$axios.$post('/api/my/account/', payload)
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
    return this.$axios.$delete('/api/my/session')
      .then((response) => {
        context.commit('logout')
      })
      .catch((e) => { console.log(e) })
  },
  getLoginStatus (context, payload) {
    return this.$axios.$get('/api/my/session')
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
