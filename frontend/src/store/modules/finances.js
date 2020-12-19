import axios from 'axios'
import Vue from 'vue'

const state = {
    is_loading: true,
    user_finances: {
        "loans": {},
        "investments": {},
        "financial_profile": {}
    }
}

const getters = {
    getFinancialProfile(state) {
        return state.user_finances.financial_profile
    },
    getFirstName(state) {
        return state.user_finances.first_name
    },
    getLastName(state) {
        return state.user_finances.last_name
    },
    getEmail(state) {
        return state.user_finances.email
    },
    getLoans(state) {
        return state.user_finances.loans
    },
    getInvestments(state) {
        return state.user_finances.investments
    },
    getLoanById: (state) => (id) => {
        return state.user_finances.loans[id]
    },
    getInvestmentById: (state) => (id) => {
        return state.user_finances.investments[id]
    }
}

const mutations = {
    setUserFinances(state, payload) {
        state.user_finances = payload
    },
    setLoan: (state, payload) => {
        Vue.set(state.user_finances.loans, payload.id, payload)
    },
    deleteLoan: (state, payload) => {
        console.log(payload)
        Vue.delete(state.user_finances.loans, payload.id)
    },
    setInvestment: (state, payload) => {
        Vue.set(state.user_finances.investments, payload.id, payload)
    },
    deleteInvestment: (state, payload) => {
        Vue.delete(state.user_finances.investments, payload.id)
    },
    setFinancialProfile: (state, payload) => {
        Vue.set(state.user_finances.financial_profile, payload)
    },
    setIsLoading: (state, payload) => {
        state.is_loading = payload
    }
}

const actions = {
    getUserFinances(context, payload) {
        return axios.get('/api/my/finances')
            .then(response => {
                context.commit('setUserFinances', response.data)
                context.commit('setIsLoading', false)
            })
            .catch(e => {
                console.log(e)
            })
    },
    createOrUpdateLoan(context, payload) {
        if (payload.id == null) {
            axios.post("/api/my/finances/loans", payload)
                .then(
                    response => {
                        context.commit("setLoan", response.data)
                    }
                )
                .catch(
                    e => {
                        console.log(e)
                    }
                )
        } else {
            axios.put(`/api/my/finances/loans/${payload.id}`, payload)
                .then(
                    response => {
                        context.commit("setLoan", response.data)
                    }
                )
                .catch(
                    e => {
                        console.log(e)
                    }
                )
        }
    },
    deleteLoan(context, payload) {
        axios.delete(`/api/my/finances/loans/${payload.id}`)
            .then(
                response => {
                    context.commit("deleteLoan", payload)
                }
            )
            .catch(
                e => {
                    console.log(e)
                }
            )
    },
    createOrUpdateInvestment(context, payload) {
        if (payload.id == null) {
            axios.post("/api/my/finances/investments", payload)
                .then(
                    response => {
                        context.commit("setInvestment", response.data)
                    }
                )
                .catch(
                    e => {
                        console.log(e)
                    }
                )
        } else {
            axios.put(`/api/my/finances/investments/${payload.id}`, payload)
                .then(
                    response => {
                        context.commit("setInvestment", response.data)
                    }
                )
                .catch(
                    e => {
                        console.log(e)
                    }
                )
        }
    },
    deleteInvestment(context, payload) {
        axios.delete(`/api/my/finances/investments/${payload.id}`)
            .then(
                response => {
                    context.commit("deleteInvestment", payload)
                }
            )
            .catch(
                e => {
                    console.log(e)
                }
            )
    },
    updateFinancialProfile (context, payload) {
        axios.post('/api/my/finances/profile', payload)
            .then(
                response => {
                    context.commit("setFinancialProfile", response.data)
                }
            )
            .catch(
                e => console.log(e)
            )
    }
}

export default {
    namespaced: true,
    state,
    getters,
    mutations,
    actions
}
