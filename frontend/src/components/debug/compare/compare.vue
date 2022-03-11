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
import { createNamespacedHelpers } from 'vuex'
const {mapMutations: mapCompareMutations,mapGetters:mapCompareGetters} = createNamespacedHelpers('compare')
export default {
    name:"compare",
    data () {
      return {
          padding:{ top: 10, right: 50, bottom: 20, left: 50 },
          index:"acc"
      }
    },
    mounted() {
      this.height = document.getElementsByClassName('plug-scalar')[0].clientHeight - 20
      this.width = document.getElementsByClassName('plug-scalar')[0].clientWidth
    },
    watch:{
      getCompare: {
        immediate: true,
        deep:true,
        handler(val) {
            this.compareData = val
            this.$nextTick(()=>{
              this.linechart()
            })
        }
      },
      index: {
        immediate: true,
        handler(val) {
            this.linechart()
        }
      },
    },
    activated(){
      this.linechart()
    },
    methods:{
      ...methods,
    },
    computed:{
      ...mapCompareGetters(['getCompare'])
    }
}
</script>
<style lang="less" scoped>
@import "compare.less";
</style>