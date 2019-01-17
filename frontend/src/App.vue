<template>
  <b-container fluid class="p-0 m-0" id="app">
    <div class="row border-0 m-0 p-0">
      <router-link id="home-link" col="col-2" to="/"
           style="font-size: 500%; color: #FF5D00;
           background-color: #2c3e50; width: 15vh; text-align: center">H</router-link>
      <div class="col border-0" style="background-color: #FF5D00;"></div>
      <auth-panel class="col-3 border-0 m-0"></auth-panel>
    </div>
    <main-menu fluid class="m-0 border-0"></main-menu>
    <router-view></router-view>
  </b-container>
</template>

<script>
import mainMenu from '@/components/Menu'
import AuthPanel from './components/AuthPanel.vue'

export default {
  name: 'App',
  components: {
    'mainMenu': mainMenu,
    'authPanel': AuthPanel
  }
}
</script>
<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

#home-link {
  font-size: 500%;
  color: #FF5D00;
  background-color: #2c3e50;
  width: 15vh;
  text-align: center
}
#home-link:hover {
  color: azure;
  text-decoration: none;
}
</style>
