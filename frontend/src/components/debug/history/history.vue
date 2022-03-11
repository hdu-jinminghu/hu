<template>
    <div :class="['history-view']">
        
        <template v-for="node in nodeList">
            <historyNodeItem :node="node" :key="`my-item-${node['uid']}`" :id="node['uid']" :attr="node['pos']"  :class="['history-item','active']" @trigerInfo="changeState"></historyNodeItem>
        </template>
        <template v-for="line in lineList">
            <historyLine :myline="line" :key="line['uid']"></historyLine>
        </template>
    </div>
</template>

<script>
import method from './history.method'
import historyNodeItem from './historyNodeItem/historyNodeItem.vue'
import historyLine from './historyLine/historyLine.vue'
import { createNamespacedHelpers } from 'vuex'
const {mapGetters: mapDebugGetters,mapMutations: mapDebugMutations,mapActions: mapDebugActions} = createNamespacedHelpers('debug')
const {mapGetters: mapScalarGetters} = createNamespacedHelpers('scalar')
const {mapGetters: mapModelViewGetters,mapActions: mapModelViewActions} = createNamespacedHelpers('modelView')
export default {
    components:{
        historyNodeItem,historyLine
    },
    data(){
        return{
            modelAmount:1,
            //  数组放置所有节点,ancestor文件路径
            nodeList:[{'uid':'item_0','ancestor':'0/1/2/3','top':'20px','left':'50px','op':'save','child':[],'pos':[0,0],'attrs':{'acc':0,'loss':0,'lr':0,'batch':0,'step':0}}],
            nodePos:[[{'uid':'item_0','ancestor':'0','top':'20px','left':'50px','op':'save','child':[],'pos':[0,0],'attrs':{'acc':0,'loss':0,'lr':0,'batch':0,'step':0}}]],
            currentItemTarget:{'uid':'item_0','ancestor':'0','top':'20px','left':'50px','op':'save','child':[],'pos':[0,0],'attrs':{'acc':0,'loss':0,'lr':0,'batch':0,'step':0}},
            lineList:[]
        }
    },
    mounted(){

    },
    methods:{
        ...method,
        ...mapDebugMutations(['setDebugDir']),
        ...mapDebugActions(['setKeepTag']),
    },
    computed:{
        ...mapDebugGetters(['getDebugDir','getConfig']),
        ...mapScalarGetters(['get_now_status']),
        ...mapModelViewGetters(['getPrunContent'])
    },
    watch:{
        getDebugDir:{
            immediate:true,
            handler(val){
                val == "save" && (function(that){
                        let attrs = {...that.getConfig,...that.get_now_status}
                        let vertex = {}
                        vertex['op'] = 'save'
                        vertex['attrs'] = attrs
                        that.addVertex(vertex)
                        that.setKeepTag({"keep":"1","dataRoute":"","structureRoute":""})
                        that.setDebugDir('')
                    })(this)
                
            }
        },
        getPrunContent:{
            immediate:true,
            handler(val){
                val == "" || (function(that){
                    let attrs = {...that.getConfig,...that.get_now_status}
                    let vertex = {}
                    vertex['op'] = val
                    vertex['attrs'] = attrs
                    that.addVertex(vertex)
                })(this)
                
            }
        }
    }
}
</script>
<style lang="less" scoped>
@import 'history.less';
</style>