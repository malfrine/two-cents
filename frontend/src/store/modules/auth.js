import router from '@/router'
import axios from 'axios'

const state = {
  loggingIn: false,
  loggedIn: false,
  profile: {},
  validation: {email: true},
  authError: false
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
  setProfile (state, payload) {
    state.profile = payload
  },
  setValidationEmail (state, bool) {
    state.validation.email = bool
  },
  setAuthError (state, bool) {
    state.loggingIn = false
    state.authError = bool
  }
}

const actions = {
  postLogin (context, payload) {
    context.commit('startLogin')
    return axios.post('/api/users/login/', payload)
      .then(response => {
        console.log(response)
        context.commit('login')
        context.dispatch('getProfile')
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
          console.log(response)
          context.commit('setValidationEmail', false)
        } else {
          context.commit('setValidationEmail', true)
          context.commit('login')
          context.commit('setProfile', response.data)
          router.push('/login')
        }
      })
      .catch(e => { console.log(e) })
  },
  getProfile (context) {
    return axios.get('/api/users/profile')
      .then(response => {
        context.commit('setProfile', response.data)
      })
      .catch(e => {
        context.commit('logout')
        console.log(e)
      })
  },
  postLogout (context, payload) {
    return axios.post('/api/users/logout/')
      .then(response => {
        console.log(context)
        context.commit('logout')
        router.push('/login')
      })
      .catch(e => {console.log(e)})
  },
  getLoginStatus (context, payload) {
    return axios.get('/api/users/check_login')
      .then(response => {
        console.log(response)
        context.commit('login')
        context.dispatch('getProfile')
        router.push('/dashboard/profile')
      })
      .catch(e => {
        context.commit('logout')
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
