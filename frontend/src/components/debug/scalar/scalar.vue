<!--
 * @Author: your name
 * @Date: 2021-04-09 15:35:46
 * @LastEditTime: 2022-02-06 15:54:29
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\components\layout\scalar.vue
-->

<template>
  <div :class="['scalar-view']">
    
    <div :class="['scalar-svg-container']"></div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import methods from './scalar.method'
import { createNamespacedHelpers } from 'vuex'
const { mapActions: mapScalarActions,mapGetters:mapScalarGetters,mapMutations: mapScalarMutations,} = createNamespacedHelpers('scalar')
export default {
    name:'scalar',
    data () {
      return {
        acc: [],
        loss: [],
        step: [],
        height:0,
        width:0
      }
    },
    mounted() {
      this.height = document.getElementsByClassName('scalar-view')[0].clientHeight -10
      this.width = document.getElementsByClassName('scalar-view')[0].clientWidth
    },
    watch:{
      get_scalar_data: {
        immediate: true,
        handler(val) {
          this.acc = val.acc
          this.loss = val.loss
          this.step = val.step
          this.breakpoints = val.breakpoints
          this.linechart()
        }
      },
    },
    activated(){
      let {fetch_scalar} = this
      this.interval = window.setInterval(function(){fetch_scalar({})},5000)
    },
    deactivated(){
      window.clearInterval(this.interval)
    },
    computed:{
      ...mapScalarGetters(["get_scalar_data"])
    },
    methods:{
        ...methods,
        ...mapScalarActions(["fetch_scalar"])
    }
}
</script>
<style lang="less" scoped>
@import "scalar.less";
</style>