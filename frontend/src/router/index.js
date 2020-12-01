import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import '../assets/scss/argon-dashboard.scss'
import 'bootstrap'

Vue.use(VueRouter)

const routes = [{
  path: '/',
  name: 'Home',
  component: Home
},
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
  component: () => import(/* webpackChunkName: "auth" */ '@/views/Login.vue')
}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
  linkExactActiveClass: 'active'
})

// router.beforeEach((to, from, next) => {
//   // redirect to login page if not logged in and trying to access a restricted page
//   const publicPages = ['/login', '/', '/coming-soon']
//   const authRequired = !publicPages.includes(to.path)
//   const loggedIn = localStorage.getItem('user')

//   if (authRequired && !loggedIn) {
//     return next('/login')
//   } else {
//     next()
//   }
// })

export default router
