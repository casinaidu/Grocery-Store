import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    categories: {}
  },
  getters: {
  },
  mutations: {
    setCategories: (state, data) => {
      state.categories = data
    }
  },
  actions: {
    async fetchCategories({ commit }) {
      const response = await fetch('http://127.0.0.1:5000/api/categories',{
      })
      console.log(response)
      const data = await response.json()
      commit('setCategories',data)
    }
  },
  modules: {
  }
})
