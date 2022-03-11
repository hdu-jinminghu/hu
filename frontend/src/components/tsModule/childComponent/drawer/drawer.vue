
<template>
        <div :class="drawer">
            <div :class="['drawer-head']">
                test_set {{acc}}/{{total}}
            </div>
            <div :class="['drawer-section']">
                <template v-for="(url,index) in urls">
                    <el-col :span="8" :key="url">
                        <div :id = "'image'+index">
                            <el-image
                                :class="imageStyle"
                                :src="url"
                                :fit="'fill'">
                            </el-image>
                        </div>
                    </el-col>
                </template>
            </div>
            <button class="fetch-button" @click="update()">fetch</button>
        </div>
</template>

<script>
import methods from "./drawer.method"
import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'
const { mapActions: mapDrawerActions,mapGetters:mapDrawerGetters} = createNamespacedHelpers('drawer')
export default {
    props:{
    },
    data () {
      return {
          drawer:{
              "drawer":true,
              "drawer-open":true,
              "drawer-close":false
          },
          urls:[],
          predict:[],
          imageStyle:{
              "image":true,
          },
          acc:0,
          total:0
      }
    },
    mounted(){
    },
    watch:{
        getImage:{
            immediate:true,
            handler(val){
                this.urls = val
                this.$nextTick(()=>{this.predic_handler()})
            }
        },
        getPredict:{
            immediate:true,
            handler(val){
                this.predict = val
                this.$nextTick(()=>{this.predic_handler()})
            }
        },
    },
    computed:{
        ...mapDrawerGetters(["getImage","getPredict"])
    },
    methods:{
        ...methods,
        ...mapDrawerActions(["fetchTestData"]),
    }
}
</script>

<style lang="less" scoped>
    @import "drawer.less";
</style>