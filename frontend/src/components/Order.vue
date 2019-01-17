<template>
  <div class="p-3">
    <div v-if="!createdOrder  && cart">
      <div style="font-size: 250%; color: #2c3e50; text-align: center">Заказ</div>
      <div class="p-2 row" v-for="(item,i) in order" :key="item.id"
           style="display: flex;align-items: center">
        <div class="col-2" style="color: crimson" v-if="messages"></div>
        <div class="col-10" style="color: crimson" v-if="messages">{{messages[item.id]}}</div>
        <div class="col-2" style="color: crimson"></div>
        <p class="col-6" style="color: #273341;"><b>{{i+1}}.</b> {{item.name}}</p>
        <div class="col-1"> </div>
        <p class="col-1" style="color: #273341;"><b>{{cart[item.id]}}шт.</b></p>
        <div class="col-1"> </div>
      </div>
      <div class="p-2 m-5" style="text-align: right;">
        <div>
          <b-button variant="warning" v-if="ALLOW_ANON_ORDERS || tokenStore" v-on:click="createOrder">
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
    <div v-else>
      <p style="font-size: 250%">Заказ № <b>{{createdOrder.id}}</b> поступил в обработку!</p>
    </div>
  </div>
</template>

<script>
import {fetchGetCartProducts, fetchCreateOrder, ALLOW_ANON_ORDERS} from '../api'
export default {
  name: 'Order',
  data () {
    return {
      cart: null,
      deliveryData: null,
      order: null,
      createdOrder: null,
      messages: null,
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
    this.$store.dispatch('inspectToken')
    this.getCartProductsAndAddress()
  },
  methods: {
    // clear sessionStorage from cart and deliveryData
    clearData: function () {
      this.cart = null
      sessionStorage.removeItem('cart')
      this.deliveryData = null
      sessionStorage.removeItem('deliveryData')
      this.order = null
    },
    // create order from cart and deliveryData from SessionStorage by sending them to backend
    // if there was some errors, it shows errors near the according product in cart
    createOrder: function () {
      const EQUAL_TO_0 = 'Ensure this value is greater than or equal to 0.'
      const EQUAL_TO_1 = 'Ensure this value is greater than or equal to 1.'
      let that = this
      let cartJSON = sessionStorage.getItem('cart')
      let deliveryDataJSON = sessionStorage.getItem('deliveryData')
      this.cart = JSON.parse(cartJSON)
      this.deliveryData = JSON.parse(deliveryDataJSON)
      if (!cartJSON || !deliveryDataJSON) {
        return 0
      }
      var data = JSON.parse(deliveryDataJSON)
      data['cart'] = JSON.parse(cartJSON)
      fetchCreateOrder(this.tokenStore, JSON.stringify(data))
        .then(function (obj) {
          if (obj.status === 200) {
            that.clearData()
            that.createdOrder = obj.body
          } else {
            that.messages = {}
            for (let i in obj.body) {
              if (obj.body[i]['quantity']) {
                for (let j in obj.body[i]['quantity']) {
                  if (obj.body[i]['quantity'][j] === EQUAL_TO_1) {
                    that.messages[i] = 'Колличество товаров этой позиции должно быть больше 0!'
                  }
                }
              } else if (obj.body[i]['stock']) {
                for (let j in obj.body[i]['stock']) {
                  if (obj.body[i]['stock'][j] === EQUAL_TO_0) {
                    that.messages[i] = 'На складе нет достаточного колличества товаров, уменьшите!'
                  }
                }
              }
            }
          }
          return obj
        }).catch(console.error.bind(console))
    },
    // get this.order( products) by sending cart from SessionStorage drom sessionStorage, fill this.cart
    // fill this.deliveryData from sessionStorage
    getCartProductsAndAddress: function () {
      let cartJSON = sessionStorage.getItem('cart')
      let deliveryDataJSON = sessionStorage.getItem('deliveryData')
      this.cart = JSON.parse(cartJSON)
      this.deliveryData = JSON.parse(deliveryDataJSON)
      if (!cartJSON) {
        var order = []
        this.order = order
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
