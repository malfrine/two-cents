import router from '@/router'
import axios from 'axios'

const state = {
  loggingIn: false,
  loggedIn: false, // only used to access private views
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
    context.commit('startLogin')
    return axios.post('/api/users/login/', payload)
      .then(response => {
        console.log(response)
        context.commit('login')
        router.push('/dashboard/profile')
      })
      .catch(e => {
        context.commit('setAuthError', true)
        console.log(e)
      })
  },
  postRegister (context, payload) {
    return axios.post('/api/users/register/', payload)
      .then(response => {
        if (response.data.status === 210) {
          // Internal server error
          console.log(response)
        } else {
          router.push('/login')
        }
      })
      .catch(e => { console.log(e) })
  },
  postLogout (context, payload) {
    return axios.post('/api/users/logout/')
      .then(response => {
        context.commit('logout')
      })
      .catch(e => {console.log(e)})
  },
  getLoginStatus (context, payload) {
    console.log("Checking log in status")
    return axios.get('/api/users/check_login')
      .then(response => {
        context.commit('login')
        router.push('/dashboard/profile')
      })
      .catch(e => {console.log(e)})
  }
}

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
}
