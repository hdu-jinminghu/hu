<!--
 * @Author: your name
 * @Date: 2020-11-09 09:21:17
 * @LastEditTime: 2021-11-23 10:33:48
 * @LastEditors: Please set LastEditors
 * @Description: 绘制矩阵
 * @FilePath: \frontend\src\components\graphs\utils\Matrix.vue
-->

<template >
<el-card :class="['card-style','box-card']">
    <div :id="id + paramData['type'] + 'div'" :class="['container']">
        <div :id="id+'digit'+paramData['type']" :class="['title-style']">step：{{paramData['step']}}</div>
        
        <div :id="id+'legend'+paramData['type']" :class="['color-bar-container']"> 
            min:{{minVal}}
            <svg id="legend" :class="['color-bar']">
                <defs>
                    <linearGradient :id="id+paramData['type']+'grad1'" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" style="stop-color:rgb(121, 163, 218);stop-opacity:1" />
                        <stop offset="50%" style="stop-color:rgb(254, 254, 190);stop-opacity:1" />
                        <stop offset="100%" style="stop-color:rgb(254, 25, 63);stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect x="3" y="6" width="100" height="10" fill="#eeeeee" />
                <rect :id="id+'legend'+paramData['type'] + 'grad1'" x="3" y="6" width="100" height="10" :fill="'url(#'+id+paramData['type']+'grad1'+')'" />
                <rect :id="id+'legend'+paramData['type'] + 'bottom'" x="0" y="3" width="3" height="16" fill="rgb(121, 163, 218)" />
                <rect :id="id+'legend'+paramData['type'] + 'top'" x="103" y="3" width="3" height="16" fill="rgb(254, 25, 63)" />
            </svg>
            max:{{maxVal}}
        </div>
            <div class="canvas-container">
                <div class = "canvas-content" >
                    <canvas :id="id" style="width:300%;height:500%">
                        您的浏览器不支持 HTML5 canvas 标签。
                    </canvas>
                </div>
            </div>
        
    </div>
</el-card>
</template>
<script>
/* eslint-disable */
import * as d3 from 'd3'
import methods from './matrix.method'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import { createNamespacedHelpers } from 'vuex'

export default {
    props: {
        paramData:{type:Object,default:{"shape":[],"type":''}},
        id:{type:String,default:""},
    },
    data() {
        return {
            scroll:true,
            rectColor: ['#79a3da', '#fefebe', '#fe193f'],
            startX: 0,
            startY: 0,
            initX: 0,
            initY: 0,
            rectScale: 1,
            tag: 0,
            xCoor: 0,
            yCoor: 0,
            longSide: 0,
            init:true,
            top: -99,
            bottom: -99,
            bottomX: 0,
            topX: 103,
            minVal:0,
            maxVal:0,
        }
    },
    mounted() {
        this.startX = 0
        this.startY = 0
        this.initX = 0
        this.initY = 0
        this.rectScale = 1
        this.tag = 0
        this.xCoor = 0
        this.yCoor = 0
        this.longSide = 0
        this.maxNum = 0
        this.drawMatrix()
    },
    watch: {
        paramData:{
            immediate: true,
            handler(val) {
                this.startX = 0
                this.startY = 0
                this.initX = 0
                this.initY = 0
                this.rectScale = 1
                this.tag = 0
                this.xCoor = 0
                this.yCoor = 0
                this.longSide = 0
                this.maxNum = 0
                this.drawMatrix()
            }
        },
    },
    methods: {
        ...methods
    }
}
</script>
<style lang="less" scoped>
@import 'matrix.less';
</style>
