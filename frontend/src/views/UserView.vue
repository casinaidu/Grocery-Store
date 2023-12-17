<template>
  <div>
    <!-- {{categories}}  -->
    <UserHeader style="padding-top:80px"></UserHeader>
    <div style="margin:30px">
      <UserCategory></UserCategory>
    </div>
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