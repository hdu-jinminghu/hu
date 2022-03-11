<template>
    <div :class="['debug-view']">
        <hyperparam></hyperparam>
        <div :class="['big-plug']">
            <history></history>
        </div>
        <div :class="['small-plug']">
            <div :class="['plug-scalar']">
                <div :class="['plug-toggle']">
                    <div :class="['toggle-button','toggle-button-active','debug-scalar']" @click="scalar_component='scalar'" >scalar</div>
                    <div :class="['toggle-button','debug-compare']" @click="scalar_component='compare'" style="marginLeft:-20px">compare</div>
                </div>
                <keep-alive>
                    <component :is="scalar_component" style="height:calc( 100% - 25px)"></component>
                </keep-alive>
            </div>
            <div :class="['plug-indicator']">
                <indicator></indicator>
            </div>
        </div>
        <div :class="['buttonList']">
            <buttonList @trigerEvent='exec'></buttonList>
        </div>
    </div>
</template>

<script>
import 'element-ui/lib/theme-chalk/index.css'
import methods from './debug.method'
import scalar from './scalar/scalar.vue'
import compare from './compare/compare.vue'
import indicator from './indicator/indicator.vue'
import buttonList from './buttonList/buttonList.vue'
import history from './history/history.vue'
import hyperparam from './hyperparam/hyperparam.vue'
import { createNamespacedHelpers } from 'vuex'
import * as d3 from "d3"
const {mapMutations: mapDebugMutations, mapActions: mapDebugActions,mapGetters: mapDebugGetters} = createNamespacedHelpers('debug')
export default {
    components:{
        scalar,compare,indicator,buttonList,history,hyperparam
    },
    data(){
        return{
            scalar_component:'scalar'
        }
    },
    computed:{
        ...mapDebugGetters(['getDebugDir'])
    },
    methods:{
        ...methods,
        ...mapDebugMutations(['setDebugDir']),
        ...mapDebugActions(['setPlayTag'])
    },
    watch:{
        getDebugDir:{
            immediate:true,
            handler(val){
                console.log(val)
                val == 'run' && this.setPlayTag({"tag":"p"});
                val == 'stop' && this.setPlayTag({"tag":"s"});
                (val == 'run' || val == 'stop') &&
                this.$nextTick(()=>{
                    console.log("p")
                    this.setDebugDir('')
                });
            }
        },
        scalar_component:{
            handler(val){
                if(val == "compare"){
                    d3.select(".debug-compare").classed("toggle-button-active",true)
                    d3.select(".debug-scalar").classed("toggle-button-active",false)
                } else {
                    d3.select(".debug-compare").classed("toggle-button-active",false)
                    d3.select(".debug-scalar").classed("toggle-button-active",true)
                }
            }
        }
    }
}
</script>

<style lang="less" scoped>
@import 'debug.less';
</style>