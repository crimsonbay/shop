<template>
  <div>
    <div class="row mx-auto m-0 p-3 border-0" id="category-main">
      <catalog-menu class="col-2" id="menu"></catalog-menu>
      <div class="col-10">
        <p style="font-size: 250%"><b>Поиск</b></p>
        <div class="col input-group-append row" style="align-items: end">
          <div class="col-1"></div>
          <input type="text" class="form-control col-5" placeholder="Enter a message..."
               aria-label="search input" aria-describedby="button-addon2"
               v-on:keyup.enter="searchButton" ref="searchInput" id="searchInput">
          <button class="btn btn-outline-secondary border-bottom-0"
                  type="button" id="button-addon2" v-on:click="searchButton"
          style="background-color: #FF5D00">Send</button>
        </div>
        <div class="row p-1 mt-3 mb-4">
          <div class="col-3" v-for="product in products" :key="product.id" v-if="product.image_thumbnail!==null">
            <router-link style="color: #2c3e50;text-decoration: none;"
                         :to="'/p/' + product.slug">
              <b-card :img-src="serverAddr+product.image_thumbnail"
                      img-alt="Image"
                      img-top
                      tag="article"
                      style="min-width: 15rem; height: 25rem;font-size: medium;text-align: center;display: flex;"
                      class="mb-2" >
                <b-card-body style="display: inherit; flex: 1; align-content: flex-end">
                  <div style=" flex: 1;">{{product.name}}</div>
                  <p style="font-size: 150%; text-align: center"><b>{{product.price}} руб.</b></p>
                  <div style="background-color: #FF5D00; height: 2rem; font-size: 120%"
                       v-on:click.self.prevent="addToCart(product, 1)">
                    В корзину
                  </div>
                </b-card-body>
              </b-card>
            </router-link>
            <modal v-show="isModalVisible" @close="closeModal">
              <template slot="body">
                <span v-html="modalMessage"></span>
              </template>
            </modal>
          </div>
        </div>
        <div style="display: flex;justify-content: center" v-if="pageCount===0">Ничего не найдено</div>
        <div style="display: flex;align-items: center;justify-content: center">
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
               v-if="currentPage!==pageCount && pageCount!==0"> &gt; </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import CatalogMenu from './CatalogMenu.vue'
import ModalAddToCart from './ModalAddToCart.vue'
import {fetchSearchProducts, serverAddr, searchLimit} from '../api'
export default {
  name: 'Search',
  components: {
    'catalogMenu': CatalogMenu,
    'modal': ModalAddToCart
  },
  data () {
    return {
      products: [], // products found for current page
      isModalVisible: false,
      modalMessage: '',
      serverAddr: serverAddr,
      pageCount: 1, // cout of our pages at backend in paginator
      currentPage: 1
    }
  },
  mounted () {
    let searchQuery = this.$route.query.q
    if (searchQuery.length > 2) {
      this.getProducts(1, searchQuery)
    }
    this.$refs.searchInput.focus()
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
    },
    // show modal window
    showModal () {
      this.isModalVisible = true
    },
    // close modal window
    closeModal () {
      this.isModalVisible = false
    },
    // if search input has more then 2 symbols, get searching products by calling getProducts
    searchButton: function () {
      if (this.$refs.searchInput.value.length > 2) {
        this.$refs.searchInput.select()
        this.getProducts(1, this.$refs.searchInput.value)
      }
    },
    // get searching products
    getProducts: function (page, searchQuery) {
      let that = this
      fetchSearchProducts(searchQuery, page)
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
</style>
