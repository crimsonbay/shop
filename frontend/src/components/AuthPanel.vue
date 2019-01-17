<template>
  <b-card no-body class="border-0 rounded-0" id="auth">
    <div v-if="firstNameStore != 'Anonymous'">
      Приветствую, {{firstNameStore}}<br>
      <button ref="buttonLogin" v-on:click="logoutClick">Logout</button>
    </div>
    <div v-else>
      <div class="text-right">
        <input type="text" class="form-control" placeholder="username..." ref="inputLogin" v-on:keyup.enter="loginClick">
        <input type="password" class="form-control" placeholder="password..." ref="inputPassword" v-on:keyup.enter="loginClick">
        <button class="mt-1" ref="buttonRegister" v-on:click="registerClick">Registration</button>
        <button class="mt-1" ref="buttonLogin" v-on:click="loginClick">Login</button>
      </div>
    </div>
  </b-card>
</template>

<script>
export default {
  name: 'AuthPanel',
  data () {
    return {
    }
  },
  computed: {
    // user token from store( токен пользователя из store)
    tokenStore () {
      return this.$store.getters.TOKEN
    },
    // first_name of user from store( first_name пользователя из store)
    firstNameStore () {
      return this.$store.getters.FIRST_NAME
    }
  },
  // after creation( после создания)
  created: function () {
    // check token( проверяем токен)
    this.$store.dispatch('checkToken')
  },
  methods: {
    registerClick: function () {
      this.$router.push('/registration')
    },
    // clicking on Logout erases their storage token
    // (нажатие на Logout стирает токен их хранилища)
    logoutClick: function () {
      this.$store.dispatch('clearToken')
    },

    // clicking on Login causes the token to be set in the store by name and password
    // (нажатие на Login вызывает установку токена в хранилище по имени и паролю)
    loginClick: function () {
      var name = this.$refs.inputLogin.value
      var password = this.$refs.inputPassword.value
      this.$store.dispatch('setToken', {username: name, password: password})
      this.$refs.inputLogin.value = ''
      this.$refs.inputPassword.value = ''
    }
  }
}
</script>

<style scoped>
  #auth {
    max-height: 50vh;
    background-color: #FF5D00;
  }
</style>
