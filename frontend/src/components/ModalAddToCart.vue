<template>
  <transition name="modal">
    <div class="modal-mask" role="dialog">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-body" style="flex-wrap: wrap;">
            <div>
              <slot name="body" style="">
                Товар ТАКОЙ-ТО добавлен в корзину
              </slot>
            </div>
            <div style="text-align: right;">
              <b-button class="modal-default-button;" @click="$emit('close')">
                  OK
              </b-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: 'ModalAddToCart',
  methods: {
    close () {
      this.$emit('close')
    }
  }
}
</script>

<style>
.modal-mask {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-body {
  width: 50vh;
  position: relative;
  padding: 20px 10px;
  background-color: beige;
  border-color: black;
  box-shadow: #23272b 2px 2px 20px 1px;
}
</style>
