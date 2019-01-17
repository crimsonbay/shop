<template>
  <div>
    <div class="row" >
      <div class="col-6" v-for="category in categoryOverview" :key="category.id">
        <b-card>
          <router-link style="color: #2c3e50" :to="'/category/' + category.slug">
            <b>{{category.name.toUpperCase()}}</b>
          </router-link>
          <li v-for="child in category.children" :key="child.id" style="color: orangered;">
            <router-link style="color: dimgrey" :to="'/category/' + category.slug + '/' + child.slug">
              {{child.name}}
            </router-link>
            {{child.group_count}}
          </li>
        </b-card>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: 'CategoryOverview',
  computed: {
    categoryOverview () {
      return this.$store.getters.CATEGORY_OVERVIEW
    }
  },
  created: function () {
    if (this.categoryOverview === null) {
      this.$store.dispatch('setCategoryOverview')
    }
  }
}
</script>

<style scoped>

</style>
