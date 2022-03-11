<!--
 * @Author: your name
 * @Date: 2021-04-10 19:16:47
 * @LastEditTime: 2021-11-23 10:09:25
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \frontend\src\components\layout\utils\confusion.vue
-->

<template>
  <div :class="['matrix-section']">
        <template v-for="data_ in matrixData_">
            <div :class="['matrix-container']" :key="data_['step']">
                <matrix
                    :paramData="data_"
                    :id="'step' + data_['step']"
                    :key="'step' + data_['step']"
                    >
                </matrix>
            </div>
        </template>
        <input v-show="n_activate_tag.endsWith('contrast')"  type="range" id="range" value="0" min="0.001" max="5" step="0.01" @change="changeMatrix()">
  </div>
</template>

<script>
import * as d3 from 'd3'
import { createNamespacedHelpers } from 'vuex'
const { mapActions: mapLayoutActions,mapGetters:mapLayoutGetters} = createNamespacedHelpers('layout')
import matrix from './matrix/matrix.vue'
import methods from './param-matrix.method'
export default {
    components: {
      matrix
    },
    props: {
        tackle_node: {type:String,defalut:""},
        isShow:{type:Boolean,default:true},
        n_activate_tag:{type:String,defalut:''}
    },
    data () {
        return{
            o_activate_tag: '',
            paramData: [],
            tag:'current',
            matrixData_:[],
            init:true,
            logIndex:-1,
            dataType:'',
            scrollTag:true,
            pos:1,
            npzList:[],
            timer:undefined
        }
    },
    computed:{
        ...mapLayoutGetters(["getWeight","getBias","getBiasGrad","getWeightGrad","getInitIndex","getTarget"])
    },
    watch:{
        isShow:{
            handler(val) {
                    this.tag = "current"
            }
        },
        n_activate_tag(val) {
            this.pos = 1
            this.scrollTag = true //操作标记
            this.init = true // 初始标记
            if(val == this.o_activate_tag) {
                return
            } else {
                const string = val.split(":")
                this.tag = string[1]
                this.dataType = string[0]
                
                if(val.match(/contrast/)){
                    this.logIndex = -1
                    this.matrixData_.splice(0,this.matrixData_.length)
                } else {
                    this.matrixData_.splice(0,this.matrixData_.length - 1)
                }
                if(val.match(/weight:/)) {
                    this.weight({"Id":this.tackle_node,"tag":string[1],"index":this.logIndex})
                } else if(val.match(/weightGrad:/)) {
                    this.weightGrad({"Id":this.tackle_node,"tag":string[1],"index":this.logIndex})
                } else if(val.match(/bias:/)) {
                    this.bias({"Id":this.tackle_node,"tag":string[1],"index":this.logIndex})
                } else if(val.match(/biasGrad:/)) {
                    this.biasGrad({"Id":this.tackle_node,"tag":string[1],"index":this.logIndex})
                }

            }
        },
        getWeight(val) {
            if(this.dataType != "weight") {
                return
            }
            var self = this
            var delay = 2000
            if(this.tag == "current") {
                this.npzList == []
                this.matrixData_.splice(0,this.matrixData_.length)
                this.matrixData_.push(val)
            } else if(this.tag == "update") {
                this.npzList == []
                const index = parseInt(val["index"])
                const tag = val["tag"]
                if(tag!="continue") {
                    this.matrixData_.splice(0,this.matrixData_.length)
                    this.matrixData_.push(val)
                    this.logIndex = index
                }
                setTimeout(function(){ self.weight({"Id":self.id,"tag":self.tag,"index":index})},delay)
            } else if(this.tag == "contrast") {
                var index = parseInt(val["index"])
                if(val["tag"] != "continue") {
                    if(val["weight"] != "none" ){
                        if(this.scrollTag){
                            this.matrixData_.splice(0,this.matrixData_.length)
                            this.matrixData_.push(val)
                            this.scrollTag = false
                        }
                        // 
                        if(val["npzList"].length != this.npzList.length || this.init){
                            this.npzList = val["npzList"]
                            let length = this.npzList.length
                            let seg = 5/length
                            this.init = false
                            d3.select("#range").property("value",this.pos*seg)
                        }
                        this.logIndex = index
                    } else {
                        delay = 200
                    }
                }
                setTimeout(function(){ self.weight({"Id":self.id,"tag":self.tag,"index":0})},delay)
            }
        },
        getWeightGrad(val) {
            if(this.dataType != "weightGrad") {
                return
            }
            var self = this
            var delay = 2000
            if(this.tag == "current") {
                this.matrixData_.splice(0,this.matrixData_.length)
                this.matrixData_.push(val)
            } else if(this.tag == "update") {
                const index = parseInt(val["index"])
                const tag = val["tag"]
                if(tag!="continue") {
                    this.matrixData_.splice(0,this.matrixData_.length)
                    this.matrixData_.push(val)
                    this.logIndex = index
                }
                setTimeout(function(){ self.weightGrad({"Id":self.id,"tag":self.tag,"index":index})},delay)
            } else if(this.tag == "contrast") {
                var index = parseInt(val["index"])
                if(val["tag"] != "continue") {
                    if(val["weightGrad"] != "none" ){
                        if(this.scrollTag){
                            this.matrixData_.splice(0,this.matrixData_.length)
                            this.matrixData_.push(val)
                            this.scrollTag = false
                        }
                        // 
                        if(val["npzList"].length != this.npzList.length || this.init){
                            this.init = false
                            this.npzList = val["npzList"]
                            let length = this.npzList.length
                            let seg = 5/length
                            d3.select("#range").property("value",this.pos*seg)
                        }
                        this.logIndex = index
                    } else {
                        delay = 200
                    }
                }
                setTimeout(function(){ self.weightGrad({"Id":self.id,"tag":self.tag,"index":0})},delay)
            }
        },
        getBias(val) {
            if(this.dataType != "bias") {
                return
            }
            var self = this
            var delay = 2000
            if(this.tag == "current") {
                this.matrixData_.splice(0,this.matrixData_.length)
                this.matrixData_.push(val)
            } else if(this.tag == "update") {
                const index = parseInt(val["index"])
                const tag = val["tag"]
                if(tag!="continue") {
                    this.matrixData_.splice(0,this.matrixData_.length)
                    this.matrixData_.push(val)
                    this.logIndex = index
                }
                setTimeout(function(){ self.bias({"Id":self.id,"tag":self.tag,"index":index})},delay)
            } else if(this.tag == "contrast") {
                var index = parseInt(val["index"])
                if(val["tag"] != "continue") {
                    if(val["bias"] != "none" ){
                        if(this.scrollTag){
                            this.matrixData_.splice(0,this.matrixData_.length)
                            this.matrixData_.push(val)
                            this.scrollTag = false
                        }
                        if(val["npzList"].length != this.npzList.length || this.init){
                            this.init = false
                            this.npzList = val["npzList"]
                            let length = this.npzList.length
                            let seg = 5/length
                            d3.select("#range").property("value",this.pos*seg)
                        }
                        this.logIndex = index
                    } else {
                        delay = 200
                    }
                }
                setTimeout(function(){ self.bias({"Id":self.id,"tag":self.tag,"index":0})},delay)
            }
        },
        getBiasGrad(val) {
            if(this.dataType != "biasGrad") {
                return
            }
            var self = this
            var delay = 2000
            console.log(this.tag)
            if(this.tag == "current") {
                this.matrixData_.splice(0,this.matrixData_.length)
                this.matrixData_.push(val)
            } else if(this.tag == "update") {
                const index = parseInt(val["index"])
                const tag = val["tag"]
                if(tag!="continue") {
                    this.matrixData_.splice(0,this.matrixData_.length)
                    this.matrixData_.push(val)
                    this.logIndex = index
                }
                console.log("update")
                setTimeout(function(){ self.biasGrad({"Id":self.id,"tag":self.tag,"index":index})},delay)
            } else if(this.tag == "contrast") {
                var index = parseInt(val["index"])
                if(val["tag"] != "continue") {
                    if(val["biasGrad"] != "none" ){
                        if(this.scrollTag){
                            this.matrixData_.splice(0,this.matrixData_.length)
                            this.matrixData_.push(val)
                            this.scrollTag = false
                        }
                        if(val["npzList"].length != this.npzList.length || this.init){
                            this.init = false
                            this.npzList = val["npzList"]
                            let length = this.npzList.length
                            let seg = 5/length
                            d3.select("#range").property("value",this.pos*seg)
                        }
                        this.logIndex = index
                    } else {
                        delay = 200
                    }
                }
                setTimeout(function(){ self.biasGrad({"Id":self.id,"tag":self.tag,"index":0})},delay)
            }
        }
    },
    methods:{
        ...mapLayoutActions([
          'weight',
          'weightGrad',
          'bias',
          'biasGrad',
          'setInitData'
        ]),
        ...methods
        
    }
}
</script>

<style lang="less" scoped>
@import 'param-matrix.less';
</style>