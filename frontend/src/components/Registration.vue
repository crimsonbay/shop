<template>
  <b-container fluid class="p-0" id="reg-all">
    <b-card id="reg-form">
      <div v-if="message!=='' &&
      message!=='You have successfully registered!( Вы успешно зарегистрировались!)'"
           style="color:#FF0000">{{message}}<br></div>
      <div v-if="
      message === 'You have successfully registered!( Вы успешно зарегистрировались!)'"
      style="color:green">{{message}}<br></div>
      Enter a name that will be displayed to other users( Введите имя, которое будет отображаться другим пользователям):
      <input type="text" class="form-control" placeholder="Name..." ref="inputName" v-on:keyup.enter="registerClick">
      Enter login( Введите логин):
      <input type="text" class="form-control" placeholder="login..." ref="inputLogin" v-on:keyup.enter="registerClick">
      Enter password( Введите пароль):
      <input type="password" class="form-control" placeholder="password..." ref="inputPass1" v-model="pass1" v-on:keyup.enter="registerClick">
      Re-enter password( Введите пароль повторно)<span style="color:#FF0000">{{passCheckMessage}}</span>:
      <input type="password" class="form-control" placeholder="password..." ref="inputPass2" v-model="pass2" v-on:keyup.enter="registerClick">
      <br>
      <div class="row justify-content-end">
        <b-button class="btn btn-default pull-right" ref="buttonLogin" v-on:click="registerClick">Registration</b-button>
      </div>
    </b-card>
  </b-container>
</template>

<script>
import { fetchAddUser } from '../api'
export default {
  name: 'Registration',
  data () {
    return {
      name: 'Registration', // name to write to the repository of the name of the open page
      // ( имя для записи в хранилище имени открытой страницы)
      message: '', // for messages( для сообщений)
      pass1: '', // first line of password( первая строчка пароля)
      pass2: '' // second line of password to match the first( вторая строчка пароля для совпадения с первой)
    }
  },
  computed: {
    // checks for password matching( проверяет совпадение паролей)
    passCheckMessage () {
      if (this.pass1 === this.pass2) {
        return ''
      } else {
        return '(passwords do not match( пароли не совпадают))'
      }
    }
  },
  // after creation( после создания)
  created: function () {
    // change the name of the open page in the repository( меняем имя открытой страницы в хранилище)
    this.$store.dispatch('setPageName', {pageName: this.name})
  },
  methods: {
    // channel name validation( валидация имени чата)
    loginValidation: function (channelName) {
      let pattern = /^[a-z0-9]+$/i
      if (!pattern.test(channelName)) {
        this.message = 'Only Latin letters and numbers are possible in login!( В login возможны только латинские буквы и цифры!)'
        this.$refs.inputLogin.value = ''
        return false
      } else {
        return true
      }
    },

    // clicking on Registration button( нажатие кнопки регистрации)
    registerClick: function () {
      let name = this.$refs.inputName.value
      let login = this.$refs.inputLogin.value
      let that = this
      if (!this.loginValidation(login)) {
        return
      }
      if (name && login && !this.passCheckMessage && this.pass1) {
        fetchAddUser(login, name, this.pass1)
          .then(function (obj) {
            if (obj.status === 400) {
              let err = obj.body['error']
              switch (err) {
                case 'UNIQUE constraint failed: auth_user.username':
                  that.$refs.inputLogin.value = ''
                  that.message = 'This login already exists, try another( Такой login уже существует, попробуйте другой)'
                  break
                default:
                  that.message = 'Unknown error!( Неизвестная ошибка!)'
              }
            } else if (obj.status === 200) {
              that.$refs.inputLogin.value = ''
              that.$refs.inputName.value = ''
              that.$refs.inputPass1.value = ''
              that.$refs.inputPass2.value = ''
              that.message = 'You have successfully registered!( Вы успешно зарегистрировались!)'
            }
            return obj
          }).catch(console.error.bind(console))
      } else if (name === '') {
        this.message = 'Name field cannot be left blank.( Поле Имя не может оставаться пустым)'
      } else if (login === '') {
        this.message = 'The login field cannot remain empty.( Поле login не может оставаться пустым)'
      } else if (this.passCheckMessage) {
        this.message = 'Passwords must match( Пароли должны совпадать)'
      } else if (this.pass1 === '') {
        this.message = 'Password must not be empty( Пароль не должен быть пустым)'
      } else {
        this.message = 'Unknown error!( Неизвестная ошибка!)'
      }
    }
  }
}
</script>

<style scoped>
#reg-all {
  height: 80vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

#reg-form {
  top: 15%;
  width: 40%;
}

.form-control {
  width: 100%;
}
</style>
