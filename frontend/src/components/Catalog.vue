<template>
  <div class="row mx-auto m-0 p-3 border-0" id="category-main">
    <catalog-menu class="col-2" id="menu"></catalog-menu>
    <router-view class="col"></router-view>
  </div>
</template>

<script>
import CatalogMenu from './CatalogMenu.vue'
export default {
  name: 'Catalog',
  components: {
    'catalogMenu': CatalogMenu
  },
  computed: {
    categories () {
      return this.$store.getters.MENU
    }
  }
}
</script>

<style scoped>
#category-main {
  background-color: beige;
  min-height: 80vh;
}
#menu {
  width: 20%;
}
a {
  color: #273341;
}
</style>
