<template>
    <svg :class="['my-line-connector']" :id="myline['uid']" :style="lineStyle">
        <defs>
            <marker id="markerArrow" markerUnits="strokeWidth" markerWidth="6" markerHeight="6" viewBox="0 0 12 12" refX="6"
                refY="6" orient="auto">
                <path d="M2,2 L10,6 L2,10 L2,2" style="fill: black;" />
            </marker>
        </defs>
    </svg>
</template>

<script>
import method from './historyLine.method'
export default {
    props:{
        myline:{type:Object,default:{}}
    },
    data(){
        return {
            lineStyle:{
                top:0,
                left:0,
                width:0,
                height:0,
                zIndex: 10,
            }
        }
    },
    watch:{
        myline:{
            immediate:true,
            handler(val){
                if(val){
                    let hniHeight = 100
                    this.lineStyle['width'] = `${parseInt(val['to_left']) - parseInt(val['from_left']) + 140}px`
                    this.lineStyle['height'] = `${parseInt(val['to_top']) - parseInt(val['from_top']) - hniHeight}px`
                    this.lineStyle['top'] = `${parseInt(val['from_top']) + hniHeight}px`
                    this.lineStyle['left'] = `${parseInt(val['from_left'])}px`
                    this.$nextTick(()=>{this.drawLine()})
                }
            }
        }
    },
    methods:{
        ...method
    }
}
</script>

<style lang="less" scoped>
@import 'historyLine.less';
</style>