<template>
  <div class="row mx-auto m-0 p-3 border-0" id="product-main">
    <catalog-menu class="col-2" id="menu"></catalog-menu>
    <div class="row col-9" v-if="product!==null">
      <p class="col-12" style="font-size: 250%"><b>{{product.name}}</b></p>
      <div class="col-8">
        <img :src="serverAddr + product.image" style="width: inherit">
      </div>
      <div class="col-4 p-3 m-0"
           style="height: 40vh;display: flex;flex-direction: column;
           background-color: white; text-align: center;">
        <p style="font-size: 150%; flex: 1"><b>{{product.name}}</b></p>
        <p style="font-size: 200%"><b>{{product.price}} руб.</b></p>
        <div>
          <span>Колличество: </span>
          <input v-model="count" type="number" value="1" size="1" min="1" max="9"><br>
        </div>
        <div class="button mt-3 p-2" style="background-color: orangered;font-size: 120%"
                 v-on:click.self.prevent="addToCart(product, 1)">
          В корзину
        </div>
        <modal v-show="isModalVisible" @close="closeModal">
          <template slot="body">
            <span v-html="modalMessage"></span>
          </template>
        </modal>
      </div>
      <div class="m-3 p-3 col-12" style="background-color: white">
        <p style="color: orangered"><b>ОПИСАНИЕ</b></p>
        <span v-html="product.description"></span>
      </div>
    </div>
  </div>
</template>

<script>
import {fetchGetProductView, serverAddr} from '../api'
import CatalogMenu from './CatalogMenu.vue'
import ModalAddToCart from './ModalAddToCart.vue'

export default {
  name: 'Product',
  components: {
    'catalogMenu': CatalogMenu,
    modal: ModalAddToCart
  },
  data () {
    return {
      isModalVisible: false,
      modalMessage: '',
      product: null,
      serverAddr: serverAddr,
      count: 1
    }
  },
  created () {
    this.GetProductView()
  },
  methods: {
    // get product by slug in path
    GetProductView () {
      let that = this
      fetchGetProductView(this.$route.params['pathMatch'])
        .then(function (obj) {
          if (obj.status === 200) {
            that.product = obj.body
          }
          return obj
        }).catch(console.error.bind(console))
    },
    // show modal window
    showModal () {
      this.isModalVisible = true
    },
    // close modal window
    closeModal () {
      this.isModalVisible = false
    },
    // add current product with count from this.count to cart
    addToCart: function (product) {
      this.modalMessage = 'Товар <b>' + product.name + '</b> добален в корзину.'
      let cart = JSON.parse(sessionStorage.getItem('cart'))
      if (!cart) {
        cart = {}
      }
      if (!cart[product.id.toString()]) {
        cart[product.id.toString()] = this.count.toString()
      } else {
        cart[product.id.toString()] = (Number(cart[product.id.toString()]) + Number(this.count)).toString()
      }
      sessionStorage.setItem('cart', JSON.stringify(cart))
      this.count = 1
      this.showModal()
    }
  }
}
</script>

<style scoped>
#product-main {
  background-color: beige;
  min-height: 80vh;
}
.button:hover {
  cursor: pointer;
}
</style>
