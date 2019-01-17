<template>
  <div>
    <div v-if="!order" style="text-align: center;font-size: 150%">Корзина пуста</div>
    <div class="p-2 m-5 row" v-for="(item,i) in order" :key="item.id"
         style="background-color: beige;display: flex;align-items: center">
      <p class="col-6" style="color: #273341;"><b>{{i+1}}.</b> {{item.name}}</p>
      <img class="col-2" :src="serverAddr+item.image_thumbnail">
      <div class="col-1"> </div>
      <p class="col-1">
        <input type="number" size="3" name="num" min="1" max="10"
               v-model="cart[item.id]"
               v-on:change="changeAmount()">
      </p>
      <div class="col-1"> </div>
      <p style="color: crimson;cursor: pointer;" v-on:click="deleteClick(item.id, i)">Удалить</p>
    </div>
    <div class="p-2 m-5" style="text-align: right;">
      <router-link to="/delivery-address">
        <b-button variant="warning"
                  v-if="(ALLOW_ANON_ORDERS || tokenStore) && order">
          Оформить
        </b-button>
      </router-link>
      <router-link to="/registration">
        <b-button variant="warning" v-if="!ALLOW_ANON_ORDERS && !tokenStore && order">
          Регистрация
        </b-button>
      </router-link>
    </div>
  </div>
</template>

<script>
import {fetchGetCartProducts, serverAddr, ALLOW_ANON_ORDERS} from '../api'
export default {
  name: 'Cart',
  data () {
    return {
      order: null,
      cart: null,
      serverAddr: serverAddr, // server address
      // registered: false,
      ALLOW_ANON_ORDERS: ALLOW_ANON_ORDERS // allow anonymous users, bool
    }
  },
  computed: {
    // user token from store( токен пользователя из store)
    tokenStore () {
      return this.$store.getters.TOKEN
    }
  },
  created () {
    this.getCartProducts()
  },
  methods: {
    // if amount in input number changed, then it changes in this.cart
    // so we write updated this.cart in sessionStorage cart
    changeAmount: function () {
      sessionStorage.setItem('cart', JSON.stringify(this.cart))
    },
    // delete position
    deleteClick: function (itemId, itemNumber) {
      delete this.cart[itemId]
      this.order.splice(itemNumber, 1)
      sessionStorage.setItem('cart', JSON.stringify(this.cart))
    },
    // get order for cart in sessionStorage
    getCartProducts: function () {
      let cartJSON = sessionStorage.getItem('cart')
      this.cart = JSON.parse(cartJSON)
      if (cartJSON === {} || cartJSON === null) {
        return 0
      }
      let that = this
      fetchGetCartProducts(this.$store.getters.TOKEN, cartJSON)
        .then(function (obj) {
          if (obj.status === 200) {
            that.order = obj.body
          }
          return obj
        }).catch(console.error.bind(console))
    }
  }
}
</script>

<style scoped>

</style>
