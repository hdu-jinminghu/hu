<template>
  <div class="compareView">
    <div class="compareScalar"></div>
    <div class="dataChange" >
        <div id="acc" class="select acc selected" @click="changeActivate('acc')"></div>
        <div id="loss" class="select loss" @click="changeActivate('loss')"></div>
    </div>
  </div>
</template>

<script>
import * as d3 from 'd3'
import methods from "./compare.method"
export default {
    props: {
      compareData: {type:Object,defalut:{}},
      height:{type:Number,defalut:0},
      width:{type:Number,defalut:0}
    },
    data () {
      return {
          padding:{ top: 10, right: 50, bottom: 20, left: 50 },
          index:"acc"
      }
    },
    mounted() {
    },
    watch:{
      compareData: {
        immediate: true,
        handler(val) {
            this.linechart()
        }
      },
      index: {
        immediate: true,
        handler(val) {
            this.linechart()
        }
      },
    },
    methods:{
      ...methods
    }
}
</script>
<style lang="less" scoped>
@import "compare.less";
</style>