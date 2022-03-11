
import Vue from 'vue'
import Router from 'vue-router'
import layout from '../components/layout/layout.vue'
import build from '../components/build/build.vue'
import debug from '../components/debug/debug.vue'
import test from '../components/test/test.vue'
import ElementUI from 'element-ui';

Vue.use(Router)
Vue.use(ElementUI);
export default new Router({
  routes: [
    {path: '/', redirect: '/index'},
    {
      path: '/index',
      name: 'Layout',
      component: layout,
      children: [
        {
          path: 'Build',
          components: {
            default: build,
          }
        },
        {
          path: 'Debug',
          components: {
            default: debug,
          }
        },
        {
          path: 'Test',
          components: {
            default: test,
          }
        },
      ]
    }
  ]
})
