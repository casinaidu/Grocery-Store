import store from "./js/store.js"

// import component1 from "./components/component1.js"
import component2 from "./components/component2.js"

// Vue.component('component1',component1)
Vue.component('component2',component2)

import router from "./js/router.js"

var app = new Vue({
  el: '#app',
  data: {
    message: 'hello'
  },
  router,
  store,
  // computed: {
  //   message() {
  //     return this.$store.state.message
  //   }
  // }
})