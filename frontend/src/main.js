/*
 * @Author: your name
 * @Date: 2021-10-23 13:13:42
 * @LastEditTime: 2021-10-26 14:48:09
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\main.js
 */
// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import Contextmenu from 'vue-contextmenujs'
import ViewUI from 'view-design'
import 'view-design/dist/styles/iview.css'
import createNamespacedHelpers from 'vuex'
import ElementUI from 'element-ui'
// import request from './utils/request'
// import port from './utils/api'

Vue.config.productionTip = false
// Vue.use(iView)
Vue.use(ViewUI)
Vue.use(ElementUI)
Vue.use(Contextmenu)
Vue.use(createNamespacedHelpers)
// Vue.prototype.$http = request
// Vue.prototype.$port = port
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
  store
})
