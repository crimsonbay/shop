<template>
  <div>
    <p style="font-size: 250%">{{message}}</p>
  </div>
</template>

<script>
import {fetchVerifyUser} from '../api'
export default {
  name: 'VerifyUser',
  data () {
    return {
      message: ''
    }
  },
  created () {
    this.getVerifyUser()
  },
  methods: {
    // calls api fetchVerifyUser, if user verified by uuid, display
    // 'Successfully verified!' else 'Something went wrong!'
    getVerifyUser () {
      let uuid = this.$route.query.uuid
      let that = this
      if (uuid) {
        fetchVerifyUser(uuid)
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
