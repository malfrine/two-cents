import Vue from 'vue'
import VueRouter from 'vue-router'
import '../assets/scss/argon-dashboard.scss'
import 'bootstrap'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
{
  path: '/coming-soon',
  name: 'Coming Soon',
  component: () =>
    import(/* webpackChunkName: "coming-soon" */ '@/views/ComingSoon.vue')
},
{
  path: '/dashboard/plan',
  name: 'DashboardPlan',
  alias: '/dashboard',
  component: () => import(/* webpackChunkName: "dash-board" */ '@/views/DashboardPlan.vue')
},
{
  path: '/dashboard/profile',
  name: 'DashboardProfile',
  component: () => import(/* webpackChunkName: "dash-board" */ '@/views/DashboardProfile.vue')
},
{
  path: '/login',
  name: 'Login',
  alias: '/',
  component: () => import(/* webpackChunkName: "auth" */ '@/views/Login.vue')
},
{
  path: '/register',
  name: 'Register',
  alias: '/',
  component: () => import(/* webpackChunkName: "auth" */ '@/views/Register.vue')
},
{
  path: '/goodbye',
  name: 'Goodbye',
  alias: '/',
  component: () => import(/* webpackChunkName: "auth" */ '@/views/Goodbye.vue')
}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  linkExactActiveClass: 'active'
})

const publicPages = ['/login', '/', '/coming-soon','/register','/goodbye']
router.beforeEach((to, from, next) => {
  // redirect to login page if not logged in and trying to access a restricted page
  const authRequired = !publicPages.includes(to.path)
  const loggedIn = store.state.auth.loggedIn
  console.log(to.path)
  console.log(from.path)
  console.log(authRequired)
  console.log(loggedIn)


  if (authRequired && !loggedIn) {
    return next('/login')
  } else {
    next()
  }
})

export default router
