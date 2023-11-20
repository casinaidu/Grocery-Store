// import router from "./js/router.js"

import component1 from "./components/component1.js"
import component2 from "./components/component2.js"

Vue.component('component1',component1)
Vue.component('component2',component2)

var app = new Vue({
  el: '#app',
  // router,
  data: {
    message: 'Hello Shab!',
    name: 'shabarish'
  },
})