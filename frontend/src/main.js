import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'

import UserHeader from '@/components/UserHeader.vue'
import UserCategory from '@/components/UserCategory.vue'
import UserProduct from '@/components/UserProduct.vue'

Vue.component('UserHeader',UserHeader)
Vue.component('UserCategory',UserCategory)
Vue.component('UserProduct',UserProduct)

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
