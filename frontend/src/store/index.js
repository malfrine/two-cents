import Vue from 'vue'
import Vuex from 'vuex'

import users from '@/store/services/users'
import auth from '@/store/modules/auth'
import { user } from '@/store/modules/user.module'
import { instruments } from '@/store/modules/instruments.module'
import { authentication } from '@/store/modules/authentication.module'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    users,
    auth,
    // authentication,
    // user,
    instruments
  }
})

export default store
