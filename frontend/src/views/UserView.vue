<template>
  <div>
    {{categories}}
  </div>
</template>

<script>
export default {
  name: 'UserView',
  computed: {
    categories() {
      return this.$store.state.categories
    },
  },
  mounted() {
    this.$store.dispatch('fetchCategories')
  }
}
</script>