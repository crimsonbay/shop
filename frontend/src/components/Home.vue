<template>
  <div class="row mx-auto m-0 p-3 border-0" id="category-main">
    <catalog-menu class="col-2" id="menu"></catalog-menu>
    <div class="col-9">
      Привет, это мой учебный проект для знакомства с технологиями.<br>
      <b>Backend:</b> Django, Django Rest Framework for API, Celery, Elasticsearch<br>
      <b>Frontend:</b> Vue.js
    </div>
  </div>
</template>

<script>
import CatalogMenu from './CatalogMenu.vue'
export default {
  name: 'Home',
  components: {
    'catalogMenu': CatalogMenu
  }
}
</script>

<style scoped>
#category-main {
  background-color: beige;
  min-height: 80vh;
}
</style>
