import Vue from 'vue'

var curLoanId = 3
var curInvestmentId = 4

export const instruments = {
  namespaced: true,
  state: {
    loans: {
      0: {
        id: 0,
        name: 'Alberta Student Loan',
        currentBalance: 5000,
        dueDate: new Date('January 1, 2028').getDate(),
        apr: 20,
        minimumMonthlyPayment: 200
      },
      1: {
        id: 1,
        name: 'Canada Student Loan',
        currentBalance: 10000,
        dueDate: new Date('January 1, 2030').getDate(),
        apr: 5,
        minimumMonthlyPayment: 200
      },
      2: {
        id: 2,
        name: 'ATB Student Line Of Credit',
        currentBalance: 20000,
        dueDate: new Date('January 1, 2035').getDate(),
        apr: 3,
        minimumMonthlyPayment: 100
      }
    },
    investments: {
      0: {
        id: 0,
        name: 'TD RRSP Mutal Fund',
        currentBalance: 0,
        apr: 3
      },
      1: {
        id: 1,
        name: 'TD TFSA Investments',
        currentBalance: 10000,
        apr: 5
      }
    }
  },
  mutations: {
    SET_LOAN: (state, payload) => { Vue.set(state.loans, payload.id, payload) },
    SET_INVESTMENT: (state, payload) => { Vue.set(state.investments, payload.id, payload) },
    UPDATE_USER: (state, payload) => {
      state.user = payload
    },
    DELETE_INVESTMENT: (state, payload) => Vue.delete(state.investments, payload.id),
    DELETE_LOAN: (state, payload) => Vue.delete(state.loans, payload.id)
  },
  actions: {
    createOrUpdateLoan ({ commit }, object) {
      // TODO: register object with backend api
      var loanId = null
      if (object.id == null) {
        curLoanId++
        loanId = curLoanId
      } else {
        loanId = object.id
      }
      commit('SET_LOAN', {
        id: loanId,
        name: object.name,
        currentBalance: object.currentBalance,
        dueDate: object.dueDate,
        apr: object.apr,
        minimumMonthlyPayment: object.minimumMonthlyPayment
      })
    },
    createOrUpdateInvestment ({ commit }, object) {
      // TODO: register object with backend api
      var investmentId = null
      if (object.id == null) {
        curInvestmentId++
        investmentId = curInvestmentId
      } else {
        investmentId = object.id
      }
      console.log(investmentId)
      commit('SET_INVESTMENT', {
        id: investmentId,
        name: object.name,
        currentBalance: object.currentBalance,
        apr: object.apr
      })
    },
    deleteInvestment ({ commit }, object) {
      // TODO: delete investment in backend
      commit('DELETE_INVESTMENT', object)
    },
    deleteLoan ({ commit }, object) {
      // TODO: delete loan in backend
      commit('DELETE_LOAN', object)
    }
  },
  getters: {
    getLoans: state => state.loans,
    getInvestments: state => state.investments,
    getInvestmentById: (state) => (id) => {
      return state.investments[id]
    },
    getLoanById: (state) => (id) => {
      return state.loans[id]
    }
  }

}
