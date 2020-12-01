export const user = {
  namespaced: true,
  state: {
    user: {
      username: 'malfy',
      email: 'malfrine@ualberta.ca',
      firstname: '',
      lastname: '',
      monthlyAllowance: 2500
    }
  },
  mutations: {
    UPDATE_USER: (state, payload) => {
      state.user = payload
    }
  },
  actions: {
    updateUser ({ commit }, object) {
      commit('UPDATE_USER', {
        username: object.username,
        email: object.email,
        firstname: object.firstname,
        lastname: object.lastname,
        monthlyAllowance: object.monthlyAllowance
      })
    }
  },
  getters: {
    getUser: state => state.user
  }

}
