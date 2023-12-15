import Vue from 'vue'
import VueRouter from 'vue-router'
import UserView from '../views/UserView.vue'
import LoginView from '../views/LoginView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'UserView',
    component: UserView
  },
  {
    path: '/login',
    name: 'LoginView',
    component: LoginView
  }
]

const router = new VueRouter({
  routes
})

export default router
