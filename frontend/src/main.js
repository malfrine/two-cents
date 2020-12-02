import Vue from 'vue'
import store from '@/store/index'
import router from '@/router/index'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserAstronaut, faMoneyBillWave, faCreditCard, faPlus, faAddressCard, faChartLine, faSignOutAlt, faEdit, faSave, faCaretDown, faCaretUp } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
library.add(faUserAstronaut, faCreditCard, faMoneyBillWave, faPlus, faAddressCard, faChartLine, faSignOutAlt, faEdit, faSave, faCaretDown, faCaretUp)

Vue.component('font-awesome-icon', FontAwesomeIcon)



import axios from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'




import VueRaven from 'vue-raven'

import App from '@/App.vue'
import './registerServiceWorker'

Vue.config.productionTip = false


// Sentry for logging frontend errors
Vue.use(VueRaven, {
  dsn: process.env.VUE_APP_SENTRY_PUBLIC_DSN,
  disableReport: process.env.NODE_ENV === 'development'
})



console.log(store)


new Vue({
  router,
  store,
  
  render: h => h(App)
}).$mount('#app')
