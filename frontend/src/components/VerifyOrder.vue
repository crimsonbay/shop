<template>
  <div>
    <p style="font-size: 250%">{{message}}</p>
  </div>
</template>

<script>
import {fetchVerifyOrder} from '../api'
export default {
  name: 'VerifyOrder',
  data () {
    return {
      message: ''
    }
  },
  created () {
    this.getVerifyOrder()
  },
  methods: {
    // calls api fetchVerifyUser, if user verified by uuid, display
    // 'Successfully verified!' else 'Something went wrong!'
    getVerifyOrder () {
      let uuid = this.$route.query.uuid
      let that = this
      if (uuid) {
        fetchVerifyOrder(uuid)
          .then(function (obj) {
            if (obj.status === 200) {
              that.message = 'Successfully verified!'
            } else {
              that.message = 'Something went wrong!'
            }
            return obj
          }).catch(console.error.bind(console))
      }
    }
  }
}
</script>

<style scoped>

</style>
