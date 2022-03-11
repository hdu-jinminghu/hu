<!--
 * @Author: your name
 * @Date: 2021-11-04 10:18:40
 * @LastEditTime: 2021-11-05 15:14:20
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\components\layout\childComponent\edit\brush.vue
-->
<template>
        <div id="editBrush" :class="brushStyle "
            v-click-outside="setNotActive"
            draggable="true"
            @dragover="allowDrop($event)"
            >
            <div class="bBorder left"></div>
            <div class="bBorder right"></div>
            <div class="bBorder top"></div>
            <div class="bBorder bottom"></div>
        </div>
        
</template>

<script>
import ClickOutside from "vue-click-outside"
import * as d3 from "d3"
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
export default {
    name:"brush",
    data(){
        return{
            brushStyle:{
                "brush":true,
                "deActive":false
            },
            initX:0,
            initY:0,
            width:0,
            height:0,
            timer:undefined
        }
    },
    directives: {
        ClickOutside
    },
    props:{
        deActiveTag:Boolean,
    },
    watch:{
        deActiveTag:{
            immediate: true,
            handler(val){
                if(val){
                    this.brushStyle["deActive"] = true
                } else {
                    this.brushStyle["deActive"] = false
                }
            }
        }
    },
    mounted(){
        this.$nextTick(()=>{this.init()})
    },
    methods:{
        setNotActive:function(){
            if(!this.brushStyle["deActive"]){
                this.getBrushWH()
                this.$emit("deActive", this.initX, this.initY, this.width, this.height)
            }
        },
        allowDrop(event) {
            event.preventDefault();
        },
        init(){
            let self = this
            d3.select(".bBorder.left").call(
                d3.drag().on('start',function _nonName(){
                    self.initMouseX = parseFloat(d3.event.sourceEvent.clientX)
                    self.initMouseY = parseFloat(d3.event.sourceEvent.clientY)
                    self.getBrushWH()
                }). 
                on('drag', function _nonName() {
                    let X = parseFloat(d3.event.sourceEvent.clientX)
                    d3.select("#editBrush").style("left",`${X - self.initMouseX + self.initX}px`)
                    d3.select("#editBrush").style("width",`${self.width - (X - self.initMouseX)}px`)
                    return false
                })
            )
            d3.select(".bBorder.right").call(
                d3.drag().on('start',function _nonName(){
                    self.initMouseX = parseFloat(d3.event.sourceEvent.clientX)
                    self.initMouseY = parseFloat(d3.event.sourceEvent.clientY)
                    self.getBrushWH()
                }). 
                on('drag', function _nonName() {
                    let X = parseFloat(d3.event.sourceEvent.clientX)
                    d3.select("#editBrush").style("width",`${self.width + (X - self.initMouseX)}px`)
                    return false
                })
            )
            d3.select(".bBorder.top").call(
                d3.drag().on('start',function _nonName(){
                    self.initMouseX = parseFloat(d3.event.sourceEvent.clientX)
                    self.initMouseY = parseFloat(d3.event.sourceEvent.clientY)
                    self.getBrushWH()
                }). 
                on('drag', function _nonName() {
                    let Y = parseFloat(d3.event.sourceEvent.clientY)
                    d3.select("#editBrush").style("top",`${Y - self.initMouseY + self.initY}px`)
                    d3.select("#editBrush").style("height",`${self.height - (Y - self.initMouseY)}px`)
                    return false
                })
            )
            d3.select(".bBorder.bottom").call(
                d3.drag().on('start',function _nonName(){
                    self.initMouseX = parseFloat(d3.event.sourceEvent.clientX)
                    self.initMouseY = parseFloat(d3.event.sourceEvent.clientY)
                    self.getBrushWH()
                }). 
                on('drag', function _nonName() {
                    let Y = parseFloat(d3.event.sourceEvent.clientY)
                    d3.select("#editBrush").style("height",`${self.height + (Y - self.initMouseY)}px`)
                    return false
                })
            )
        },
        getBrushWH(){
            this.initX = parseFloat(d3.select("#editBrush").style("left"))
            this.initY = parseFloat(d3.select("#editBrush").style("top"))
            this.width = parseFloat(d3.select("#editBrush").style("width"))
            this.height = parseFloat(d3.select("#editBrush").style("height"))
            return {"x":this.initX,"y":this.initY,"width":this.width,"height":this.height}
        }
    }
}

</script>

<style lang="less" scoped>
.brush{
    position: absolute;
    border: 1px solid lightblue;
    background-color: transparent;
    width: 50px;
    height: 50px;
}
.deActive{
    display: none;
}
.bBorder{
    z-index: 99;
    position: absolute;
    font-size: 0.1px;
}
.top{
    top: -5px;
    height: 7px;
    width: 100%;
    left: 0%;
    cursor: s-resize;
}
.left{
    top: 0px;
    left: -5px;
    height: 100%;
    width: 7px;
    cursor: e-resize;
}
.bottom{
    bottom: -5px;
    left: 0px;
    height: 7px;
    width: 100%;
    cursor: s-resize;
}
.right{
    top: 0px;
    right: -5px;
    height: 100%;
    width: 7px;
    cursor: e-resize;
}
// .cover{
//     height: 100vh;
//     width: 100vw;
//     background-color: black;
//     opacity: 0.5;
//     z-index: 3000;
// }
</style>