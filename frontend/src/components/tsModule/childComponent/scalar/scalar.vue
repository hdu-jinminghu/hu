<!--
 * @Author: your name
 * @Date: 2021-04-09 15:35:46
 * @LastEditTime: 2021-11-22 15:15:51
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\components\layout\scalar.vue
-->

<template>
  <div id="view">
    
    <div id="scalar"></div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import methods from './scalar.method'
import { createNamespacedHelpers } from 'vuex'
const { mapActions: mapScalarActions,mapGetters:mapScalarGetters,mapMutations: mapScalarMutations,} = createNamespacedHelpers('scalar')
export default {
    props: {
      height:{type:Number,defalut:0},
      width:{type:Number,defalut:0},
      editPage:{type:Boolean,default:false}
    },
    data () {
      return {
        acc: [],
        loss: [],
        step: [],
      }
    },
    mounted() {
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
      editPage:{
        immediate: true,
        handler(val) {
          let {fetch_scalar} = this
          if(!val){
            this.interval = window.setInterval(function(){fetch_scalar({})},5000)
          } else {
            window.clearInterval(this.interval)
          }
        }
      }
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