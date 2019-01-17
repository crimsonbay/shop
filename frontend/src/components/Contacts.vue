<template>
  <div class="row mx-auto m-0 p-3 border-0" id="contacts-main">
    <catalog-menu class="col-2" id="menu"></catalog-menu>
    <iframe class="col-9" src="https://yandex.ru/map-widget/v1/?um=constructor%3Abf75ee14d01614486af3fccf57bf23e4c06eef67e86cea059794b6baf2a73b78&amp;source=constructor" width="910" height="470" frameborder="0"></iframe>
  </div>
</template>

<script>
import CatalogMenu from './CatalogMenu.vue'
export default {
  name: 'Contacts',
  components: {
    'catalogMenu': CatalogMenu
  }
}
</script>

<style scoped>
#contacts-main {
  background-color: beige;
  min-height: 80vh;
}
</style>
