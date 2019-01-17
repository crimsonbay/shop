<template>
  <div class="p-0">
    <div id="category-menu">
      <b-nav vertical class="col-3 text-white p-0 m-0 border-top-0 border-bottom-0">
        <div v-for="category in categories" :key="category.id" v-if="category!==[]">
          <b-nav-item class="menu-item m-0 p-1">
            <router-link :to="'/category/' + category.slug">
              <p class="m-0 p-0"><b>{{category.name.toUpperCase()}}</b></p>
            </router-link>
          </b-nav-item>
        </div>
      </b-nav>
    </div>
    <br>
    <div style="text-align: center; background-color: white">
      Наш адрес:<br>
г. Санкт-Петербург,<br>
ул. Ивана Сусанина,<br>
д. 999
Режим работы:<br>
Пн-Пт: с 10.00 до 18.00<br>
Сб: с 12.00 до 17.00<br>
Вс: выходной
    </div>
  </div>
</template>

<script>
export default {
  name: 'CatalogMenu',
  computed: {
    categories () {
      return this.$store.getters.MENU
    }
  }
}
</script>

<style scoped>
#category-menu {
  height: auto;
  background-color: white;
  border: 1px solid #273341;
}
.menu-item {
  text-align: left;
  color: #273341;
}
a {
  color: #273341;
}
</style>
