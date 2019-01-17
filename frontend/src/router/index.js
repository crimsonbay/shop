import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import Catalog from '../components/Catalog'
import CategoryOverview from '../components/CategoryOverview.vue'
import SubCategory from '../components/SubCategory.vue'
import Cart from '../components/Cart'
import Registration from '../components/Registration'
import DeliveryAddress from '../components/DeliveryAddress'
import Order from '../components/Order'
import Search from '../components/Search'
import Delivery from '../components/Delivery'
import Contacts from '../components/Contacts'
import Home from '../components/Home'
import VerifyUser from '../components/VerifyUser'
import Product from '../components/Product'
import VerifyOrder from '../components/VerifyOrder'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/category',
      // name: 'Catalog',
      component: Catalog,
      children: [
        {
          path: '',
          name: 'CategoryOverview',
          component: CategoryOverview
        },
        {
          path: '*',
          name: 'SubCategory',
          component: SubCategory
        }
      ]
    },
    {
      path: '/cart',
      name: 'Cart',
      component: Cart
    },
    {
      path: '/registration',
      name: 'Registration',
      component: Registration
    },
    {
      path: '/delivery-address',
      name: 'DeliveryAddress',
      component: DeliveryAddress
    },
    {
      path: '/order',
      name: 'Order',
      component: Order
    },
    {
      path: '/search',
      name: 'Search',
      component: Search
    },
    {
      path: '/delivery',
      name: 'Delivery',
      component: Delivery
    },
    {
      path: '/contacts',
      name: 'Contacts',
      component: Contacts
    },
    {
      path: '',
      name: 'Home',
      component: Home
    },
    {
      path: '/verify-user',
      name: 'VerifyUser',
      component: VerifyUser
    },
    {
      path: '/verify-order',
      name: 'VerifyOrder',
      component: VerifyOrder
    },
    {
      path: '/p/*',
      name: 'Product',
      component: Product
    }
  ]
})
