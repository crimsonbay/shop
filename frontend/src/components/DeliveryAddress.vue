<template>
  <div class="p-3">
    <div style="font-size: 250%; color: #2c3e50;">Данные для доставки</div>
    <div class="row">
      <div class="col-3"></div>
      <div class="col-6">
        <p class="mb-2">Введите <b>имя</b>:</p>
        <input type="text" class="form-control mb-3" placeholder="First Name..." ref="inputFirstName">
        <p class="m-2">Введите <b>фамилию</b>:</p>
        <input type="text" class="form-control mb-3" placeholder="Last Name..." ref="inputLastName">
        <p class="mb-2">Введите <b>email</b> для связи:</p>
        <input type="text" class="form-control mb-3" placeholder="First Name..." ref="inputEmail">
        <p class="mb-2">Введите <b>город</b>:</p>
        <input type="text" class="form-control mb-3" placeholder="First Name..." ref="inputCity">
        <p class="mb-2">Введите <b>адрес</b>:</p>
        <input type="text" class="form-control mb-3" placeholder="First Name..." ref="inputAddress">
        <p class="mb-2">Введите <b>почтовый индекс</b>:</p>
        <input type="text" class="form-control mb-3" placeholder="First Name..." ref="inputPostalCode">
      </div>
    </div>
    <div class="p-2 m-5" style="text-align: right;">
      <div>
        <b-button variant="warning"
                  v-if="(ALLOW_ANON_ORDERS || tokenStore) && cart!==null"
                  v-on:click="clickIssueButton">
          Оформить
        </b-button>
      </div>
      <router-link to="/registration">
        <b-button variant="warning" v-if="!ALLOW_ANON_ORDERS && !tokenStore">
          Регистрация
        </b-button>
      </router-link>
    </div>
  </div>
</template>

<script>
import {fetchGetLastAddress, ALLOW_ANON_ORDERS} from '../api'
export default {
  name: 'DeliveryAddress',
  data () {
    return {
      address: {},
      // registered: false,
      cart: null,
      ALLOW_ANON_ORDERS: ALLOW_ANON_ORDERS // if true, it don't need to be auth user to create order
    }
  },
  computed: {
    // user token from store( токен пользователя из store)
    tokenStore () {
      return this.$store.getters.TOKEN
    }
  },
  created () {
    if (this.TokenStore) {
      this.fillAddress()
    } else {
      let cartJSON = sessionStorage.getItem('cart')
      this.cart = JSON.parse(cartJSON)
    }
  },
  methods: {
    // when issueButton click, fill deliveryData from address inputs in sessionStorage
    clickIssueButton: function () {
      let deliveryData = {}
      deliveryData['firstName'] = this.$refs.inputFirstName.value
      deliveryData['lastName'] = this.$refs.inputLastName.value
      deliveryData['email'] = this.$refs.inputEmail.value
      deliveryData['city'] = this.$refs.inputCity.value
      deliveryData['address'] = this.$refs.inputAddress.value
      deliveryData['postal_code'] = this.$refs.inputPostalCode.value
      sessionStorage.setItem('deliveryData', JSON.stringify(deliveryData))
      this.$router.push('Order')
    },
    // only for authenticated users, looking for last order,
    // if find return it's address name and other delivery info
    // if not auth, backend send HTTP_401_UNAUTHORIZED, nofing changes
    fillAddress: function () {
      let cartJSON = sessionStorage.getItem('cart')
      this.cart = JSON.parse(cartJSON)
      if (!cartJSON) {
        return 0
      }
      let that = this
      fetchGetLastAddress(this.$store.getters.TOKEN)
        .then(function (obj) {
          if (obj.status === 200) {
            that.$refs.inputFirstName.value = obj.body['first_name']
            that.$refs.inputLastName.value = obj.body['last_name']
            that.$refs.inputEmail.value = obj.body['email']
            that.$refs.inputCity.value = obj.body['city']
            that.$refs.inputAddress.value = obj.body['address']
            that.$refs.inputPostalCode.value = obj.body['postal_code']
          }
          return obj
        }).catch(console.error.bind(console))
    }
  }
}
</script>

<style scoped>

</style>
