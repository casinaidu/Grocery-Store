import view1 from '../views/view1.js'
import view2 from '../views/view2.js'
import view3 from '../views/view3.js'

Vue.component('view1',view1)
Vue.component('view2',view2)
Vue.component('view3',view3)

const routes = [{
    path: '/',
    component: view1,
}, {
    path: '/about',
    component: view2
}, {
    path: '/privacy-policy',
    component: view3
}];

const router = new VueRouter({
  routes // short for `routes: routes`
})

export default router