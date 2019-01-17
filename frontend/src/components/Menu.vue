<template>
  <b-container fluid>
    <b-nav class="row text-white border-0" id="menu">
      <router-link to="/category" class="menu-item menu-text p-2" style="text-align: center">ТОВАРЫ</router-link>
      <router-link to="/delivery" class="menu-item menu-text p-2" style="text-align: center">ДОСТАВКА</router-link>
      <router-link to="/contacts" class="menu-item menu-text p-2" style="text-align: center">КОНТАКТЫ</router-link>
      <router-link to="/cart" class="menu-item menu-text p-2" style="text-align: center">КОРЗИНА</router-link>
      <div class="col-2"></div>
      <div class="col input-group-append" style="align-items: end">
        <input type="text" class="form-control" placeholder="Enter a query..."
             aria-label="Recipient's username" aria-describedby="button-addon2"
             v-on:keyup.enter="goSearch" ref="textInput" id="textInput">
        <button class="btn btn-outline-secondary border-bottom-0"
                type="button" id="button-addon2" v-on:click="goSearch">Send</button>
      </div>
    </b-nav>
  </b-container>
</template>

<script>
export default {
  name: 'Menu',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  created: function () {
    this.$store.dispatch('setMenu')
  },
  methods: {
    // route to search page, clear search text input
    goSearch: function () {
      this.$router.push({ path: '/search', query: { q: this.$refs.textInput.value } })
      this.$refs.textInput.value = ''
    }
  }
}
</script>

<style scoped>
#menu {
  background-color: #273341;
  max-height: 5vh;
  text-align: center;
}

.menu-item {
  width: 13%;
  height: 40px;
  color: #273341;
}
.menu-item:hover {
  text-decoration: none;
  background-color: #FF5D00;
}

.drop-menu-item {
  text-align: left;
  height: 40px;
  color: #273341;
}
.drop-menu-item:hover {
  color: orangered;
}
.menu-text {
  text-align: left;
  color: azure;
  font-family: Ubuntu, Arial, Helvetica, sans-serif;
  justify-items: center;
}
.menu-text:hover{
}
</style>
