<template>
  <div class="row mx-auto m-0 p-3 border-0" id="delivery-main">
    <catalog-menu class="col-2" id="menu"></catalog-menu>
    <div class="col-9">
      <p style="font-size: 250%"><b>Условия доставки</b></p>
      <p style="color: crimson">Внимание!
Доставка осуществляется в течение 3-х дней с момента получения клиентом уведомления о готовности товара.
Неверно предоставленный Вами номер телефона, неточный или неполный адрес могут привести к дополнительной задержке и затратам с Вашей стороны! Внимательно заполняйте ваши персональные данные при оформлении заказа на сайте или при оформлении договора. Конфиденциальность ваших данных гарантируется.</p>
       <b>Доставка осуществляется:</b><br>
Будние дни&nbsp;Пн-Пт&nbsp;с 14:00 до 18:00<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; с 18:00 до 23:00<br>
Выходные дни Сб   с 14:00 до 18:00<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; с 18:00 до 23:00
      <p style="color: crimson">Воскресенье выходной день – отгрузка не осуществляется. </p>
      Если товар имеется в наличии на складе, то доставка производится в течение 1-3х дней с момента оформления заказа.
    </div>
  </div>
</template>

<script>
import CatalogMenu from './CatalogMenu.vue'
export default {
  name: 'Delivery',
  components: {
    'catalogMenu': CatalogMenu
  }
}
</script>

<style scoped>
#delivery-main {
  background-color: beige;
  min-height: 80vh;
}
</style>
