<template>
  <div>
    <div class="m-1" style="display: inline-block;background-color: white">
        <router-link style="color: #2c3e50" to="/">
          <b>ГЛАВНАЯ ></b>
        </router-link>
    </div>
    <div class="m-1" style="display: inline-block;background-color: white">
        <router-link style="color: #2c3e50" to="/category/">
          <b>ТОВАРЫ ></b>
        </router-link>
    </div>
    <div class="m-2" v-for="parent in paths" :key="parent.id"
         style="display: inline-block;" v-if="category.name">
      <div style="background-color: white">
        <router-link style="color: #2c3e50" :to="'/category' + parent.path">
          <b>{{parent.name.toUpperCase()}} ></b>
        </router-link>
      </div>
    </div>
    <div class="m-1" style="display: inline-block;background-color: white" v-if="category.name">
        <div style="color: #2c3e50">
          <b>{{category.name.toUpperCase()}}</b>
        </div>
    </div>
    <p style="font-size: 250%"><b>{{category.name}}</b></p>
    <div class="row">
      <div class="col-3" v-for="chield in category.children" :key="chield.id" v-if="chield.image!==null">
        <router-link style="color: #2c3e50;text-decoration: none;"
                     :to="'/category/' + $route.params['pathMatch'] + '/' + chield.slug">
          <b-card :img-src="serverAddr + chield.image"
                  img-alt="Image"
                  img-top
                  tag="article"
                  style="max-width: 20rem;"
                  class="mb-2" >
            {{chield.name}}
          </b-card>
        </router-link>
      </div>
    </div>
    <div class="p-1 mt-3 mb-4" style="background-color: white">
      <div class="m-1" style="color: black;display: inline-block;">Сортировать по:</div>
      <div class="m-1" style="display: inline-block;cursor: pointer" v-on:click="changeSort('default')">
        <p class="m-0 p-0" style="display: inline-block;color: orangered" v-if="sort_by===DEFAULT_SORT">По умолчанию</p>
        <p class="m-0 p-0" style="display: inline-block;color: gray" v-if="sort_by!==DEFAULT_SORT">По умолчанию</p>
      </div>
      <div class="m-1" style="display: inline-block;cursor: pointer" v-on:click="changeSort('price')">
        <p class="m-0 p-0" style="display: inline-block;color: gray" v-if="sort_by===DEFAULT_SORT">По цене</p>
        <p class="m-0 p-0" style="display: inline-block;color: orangered" v-if="sort_by===BY_PRICE_SORT">По цене↑</p>
        <p class="m-0 p-0" style="display: inline-block;color: orangered" v-if="sort_by===BY_PRICE_REVERSE_SORT">По цене↓</p>
      </div>
    </div>
    <div class="row">
      <div class="col-3" v-for="product in products" :key="product.id" v-if="product.image_thumbnail!==null">
        <router-link style="color: #2c3e50;text-decoration: none;"
                     :to="'/p/' + product.slug">
          <div class="mb-2 rounded border" id="cards">
            <img class="" :src="product.image_thumbnail" style="width: 100%;">
            <div style="flex:1;">{{product.name}}</div>
            <p style="font-size: 150%;"><b>{{product.price}} руб.</b></p>
            <div class="m-1" style="background-color: #FF5D00; height: 2rem; font-size: 120%"
                 v-on:click.self.prevent="addToCart(product, 1)">
              В корзину
            </div>
          </div>
        </router-link>
        <modal v-show="isModalVisible" @close="closeModal">
          <template slot="body">
            <span v-html="modalMessage"></span>
          </template>
        </modal>
      </div>
      <p>&nbsp;</p>
      <div class="col-12"
           style="display: flex;flex-wrap: wrap;align-items: center;justify-content: center">
          <div class="p-2 mr-3 page-button"
               v-on:click="pageButton('<')"
               v-if="currentPage!==1"> &lt; </div>
          <div v-for="i in pageCount" :key="i">
            <div class="p-2 mr-3 page-button"
                 style="background-color: #FF5D00;border-radius: 8px;color: azure;"
                 v-if="i===currentPage">{{i}}</div>
            <div class="p-2 mr-3 page-button" v-else v-on:click="pageButton(i)">{{i}}</div>
          </div>
          <div class="p-2 mr-3 page-button"
               v-on:click="pageButton('>')"
               v-if="currentPage!==pageCount"> &gt; </div>
        </div>
    </div>
  </div>
</template>

<script>
import {fetchGetCategory, fetchGetProducts, searchLimit, serverAddr} from '../api'
import ModalAddToCart from './ModalAddToCart.vue'
export default {
  name: 'SubCategory',
  components: {
    modal: ModalAddToCart
  },
  data () {
    return {
      category: [], // category with subcategories with small images from path
      paths: [], // path ancestors of category
      DEFAULT_SORT: '',
      BY_PRICE_SORT: '&sort=price',
      BY_PRICE_REVERSE_SORT: '&sort=reverse_price',
      sort_by: '', // type of our sort to display products
      products: [], // products for category and it's subcategories for current page
      isModalVisible: false,
      modalMessage: '',
      pageCount: 1, // cout of our pages at backend in paginator
      currentPage: 1,
      serverAddr: serverAddr
    }
  },
  created () {
    this.getCategory()
  },
  watch: {
    $route (to, from) {
      this.getCategory()
    },
    category: [
      'setPaths',
      'getProducts'
    ]
  },
  methods: {
    // page turning when corresponding button pressed
    pageButton (buttonName) {
      if (buttonName === '<') {
        this.currentPage -= 1
      } else if (buttonName === '>') {
        this.currentPage += 1
      } else {
        this.currentPage = buttonName
      }
      this.getProducts()
    },
    // show modal window
    showModal () {
      this.isModalVisible = true
    },
    // close modal window
    closeModal () {
      this.isModalVisible = false
    },
    // add product to cart and show modal window about it
    addToCart: function (product, count) {
      this.modalMessage = 'Товар <b>' + product.name + '</b> добален в корзину.'
      let cart = JSON.parse(sessionStorage.getItem('cart'))
      if (!cart) {
        cart = {}
      }
      if (!cart[product.id.toString()]) {
        cart[product.id.toString()] = count.toString()
      } else {
        cart[product.id.toString()] = (Number(cart[product.id.toString()]) + count).toString()
      }
      sessionStorage.setItem('cart', JSON.stringify(cart))
      this.showModal()
    },
    // change sort if one of sort button press
    changeSort: function (method) {
      if (method === 'default' && this.sort_by !== this.DEFAULT_SORT) {
        this.sort_by = this.DEFAULT_SORT
      } else if (method === 'price') {
        if (this.sort_by !== this.BY_PRICE_SORT) {
          this.sort_by = this.BY_PRICE_SORT
        } else {
          this.sort_by = this.BY_PRICE_REVERSE_SORT
        }
      }
      this.getProducts()
    },
    // fill this.category with a category with subcategories with small images from path
    getCategory: function () {
      let that = this
      fetchGetCategory(this.$route.params['pathMatch'])
        .then(function (obj) {
          if (obj.status === 200) {
            that.category = obj.body
          }
          return obj
        }).catch(console.error.bind(console))
    },
    // fill this.paths with path to category
    setPaths: function () {
      let path = ''
      this.paths = []
      let categoryPath = this.category.path
      for (let i in categoryPath) {
        let item = {}
        path += '/' + categoryPath[i].slug
        item.path = path
        item.name = categoryPath[i].name
        this.paths.push(item)
      }
    },
    // fill this.products that have the category
    // or it's subcategory, category takes like the simbols after last slash in path
    // optional parameter this.sort_by can sort by price or reverse price
    getProducts: function () {
      let that = this
      fetchGetProducts(this.$route.params['pathMatch'], this.currentPage, this.sort_by)
        .then(function (obj) {
          if (obj.status === 200) {
            that.products = obj.body.results
            that.pageCount = Math.ceil(obj.body.count / searchLimit)
          }
          return obj
        }).catch(console.error.bind(console))
    }
  }
}
</script>

<style scoped>
.page-button:hover {
  background-color: #FF5D00;
  border-radius: 8px;
  color: azure;
  cursor: pointer;
}
#cards {
  min-width: 15rem;
  height: 25rem;
  font-size: medium;
  text-align: center;
  display: flex;
  flex-direction: column;
  border: 1px;
  border-color: #273341;
}
</style>
