<template>
    <div 
        :class="['hni-node-item']" 
        :style="flowNodeContainer" 
        @click="bubbleInfo()" 
        @mouseenter="showFullOp($event)"
        @mouseout="reset($event)"
        @contextmenu.prevent="onContextmenu"
    >
    <div :class="['hni-mark']" :style="markStyle"></div>
    <div :class="['hni-op']">
        <div :class="['hni-op-content']" :style="savedStyle">{{node['op']|opcontent}}</div>
        <div :class="['hni-op-content']">{{node['op']|detail}}</div>
    </div>
    <div :class="['hni-attrs-container']">
        <div :class="['hni-item']">step:{{node['attrs']['step']}}</div>
        <div :class="['hni-item']">lr:{{node['attrs']['lr']}}</div>
        <div :class="['hni-item']">batch:{{node['attrs']['batch']}}</div>
        <div :class="['hni-item']">loss:{{node['attrs']['loss']}}</div>
        <div :class="['hni-item']">acc:{{node['attrs']['acc']}}</div>
    </div>
    </div>
</template>

<script>
import method from './historyNodeItem.method'
import { createNamespacedHelpers } from 'vuex'
const {mapGetters: mapDebugGetters, mapMutations: mapDebugMutations} = createNamespacedHelpers('debug')
const {mapActions: mapCompareActions, mapMutations: mapCompareMutations} = createNamespacedHelpers('compare')
const {mapGetters: mapModelViewGetters,mapActions: mapModelViewActions} = createNamespacedHelpers('modelView')
export default {
    props:{
        node:{type:Object,default:{}}
    },
    data(){
        return{
            flowNodeContainer:{
                top:0,
                left:0
            },
            markStyle:{
                backgroundColor:'transparent'
            },
            savedStyle:{

            }
        }
    },
    computed:{
        ...mapDebugGetters(['getCompareColor']),
    },
    filters: {
        opcontent: function (value) {
            let op = value.split(" ")
            return op[0]
        },
        detail: function (value) {
            let op = value.split(" ")
            return op[1]
        },
    },
    watch:{
        node:{
            immediate:true,
            handler(val){
                this.flowNodeContainer['top'] = val['top']
                this.flowNodeContainer['left'] = val['left']
                let op = val['op'].split(" ")
                if(op.length == 1){
                    this.savedStyle["height"] = '30px'
                    this.savedStyle["lineHeight"] = '30px'
                    this.savedStyle["fontSize"] = '14px'
                }
                this.dealgraph({"uid":val["uid"],"op":"save"})
            }
        }
    },
    mounted(){
    },
    methods:{
        ...method,
        ...mapCompareActions(['fetchTrainData']),
        ...mapCompareMutations(['delTrainData']),
        ...mapModelViewActions(['dealgraph']),
        ...mapDebugMutations(['setLr','setBatch'])
    }
}
</script>

<style lang="less" scoped>
@import 'historyNodeItem.less';
</style>