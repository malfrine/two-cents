import Vue from 'vue'
import Vuex from 'vuex'

import auth from '@/store/modules/auth'
import finances from '@/store/modules/finances'
import { instruments } from '@/store/modules/instruments.module'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    auth,
    instruments,
    finances
  }
})

export default store
