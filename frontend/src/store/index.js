import Vue from 'vue'
import Vuex from 'vuex'

import users from '@/store/services/users'
import auth from '@/store/modules/auth'
import { instruments } from '@/store/modules/instruments.module'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    users,
    auth,
    instruments
  }
})

export default store
