<!--
 * @Author: your name
 * @Date: 2021-12-06 12:01:36
 * @LastEditTime: 2022-02-08 18:18:33
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: \frontend\src\components\layout\childComponent\listPanel\listPanel.vue
-->

<template>
<div :class="['list-container']">
    <!-- <div :class="['contorl-panel']">
        <div :class="['contorller']">
            <div :class="['input']">
                <div :class="['skeleton']">
                    <input v-model="config['skeleton']" type="text" name="fname" placeholder="skeleton"/>
                </div>
                <div :class="['image-shape']">
                    <input v-model="config['image']" type="text" name="fname" placeholder="input size"/>
                </div>
            </div>
            <div :class="['config']">
                <div :class="['config-tiem']">
                    <div :class="['item-title']">depth</div>
                    <input v-model="config['depth']" type="text" name="fname" />
                </div>
                <div :class="['config-tiem']">
                    <div :class="['item-title']">epoch</div>
                    <input v-model="config['epoch']" type="text" name="fname" />
                </div>
                <div :class="['config-tiem']">
                    <div :class="['item-title']">tol</div>
                    <input v-model="config['tol']" type="text" name="fname" />
                </div>
                <div :class="['config-tiem']">
                    <div :class="['item-title']">acc</div>
                    <input v-model="config['acc']" type="text" name="fname" />
                </div>
                <div :class="['config-tiem']">
                    <div :class="['item-title']">loss</div>
                    <input v-model="config['loss']" type="text" name="fname" />
                </div>
            </div>
        </div>
        <div :class="['on-button']" @click="automlProcessExec()"><i v-if="automlBegin" class="el-icon-loading"></i></div>
    </div> -->
    <div :class="['title']">
        <!-- <div :class="['model-id']">id</div> -->
        <div :class="['model-id']"></div>
        <div :class="['performance-group']">performance
            <div :class="['sort-button-group']">
                <div :class="['sort-button','sort-acc','sort-active']" @click="sortModel(0)">acc</div>
                <div :class="['sort-button','sort-loss','sort-deactive']" @click="sortModel(1)">loss</div>
                <div :class="['sort-button','sort-size','sort-deactive']" @click="sortModel(2)">size</div>
            </div>
        </div>
        <div style="text-align:center;width:50px;lineHeight:46px">check</div>
        <!-- <div :class="['refresh']" @click="fetchAutomlList()"><i class="el-icon-refresh"></i></div> -->
        <div :class="['refresh']" @click="fetchAutomlList()">{{model_list.length}}/{{getTol}}</div>
    </div>
    <div :class="['model-list']">
        <template v-for="model in model_list">
            <div :class="['list-item']"  :key="model[3]">
                <div :class="['model-id']">id:{{model[3]}}</div>
                <div :class="['model-performance','model-acc']">{{model[0]}}</div>
                <div :class="['model-performance','model-loss']">{{model[1]}}</div>
                <div :class="['model-performance','model-size']">{{model[2]}}</div>
                <div :class="['check_box']" @click="check_model($event,model[3])"></div>
            </div>
        </template>
    </div>
</div>
</template>

<script>
import * as d3 from 'd3'
import methods from './listPanel.methods'
import { createNamespacedHelpers } from 'vuex'
const {mapGetters:mapListPanelGetters,mapMutations: mapListPanelMutations,mapActions: mapListPanelActions} = createNamespacedHelpers('listPanel')
const {mapMutations: mapEditorMutations} = createNamespacedHelpers('editor')
const {mapGetters: mapModelViewMutations} = createNamespacedHelpers('modelView')
export default ({
    props:{
        on_off:{type:Boolean,defalut:false},
    },
    data(){
        return {
            sortKey:0,
            tol:10,
            finished:20,
            model_list:[],
            timer:null,
            config:{
                "skeleton":'',
                "image":'',
                "depth":0,
                "epoch":0,
                "tol":0,
                "acc":0,
                "loss":0
            },
            automlBegin:false,
        }
    },
    mounted(){
        setInterval(()=>{
            this.fetchAutomlList();
        },5000)
    },
    watch:{
       on_off:{
           immediate:true,
           handler(val){
               if(val){
                   
               }
           }
       },
       getAutomlList:{
           immediate:true,
           handler(val){
               this.model_list = val
               d3.select(".refresh").classed(".refresh-run",false)
           }
       },
       getAutomlGraph:{
            handler(val){
                window.jsPlumb.Defaults.env = "adjust";
                this.layout(val);
                this.$nextTick(()=>{this.set_graph(val)});
            }
       }
    },
    computed:{
        ...mapListPanelGetters(["getAutomlList","getAutomlGraph"]),
        ...mapModelViewMutations(["getTol"])
    },
    methods:{
        ...methods,
        ...mapListPanelActions(["fetchAutomlData", "fetchAutomlModelGraph","automlProcess"]),
        ...mapEditorMutations(["set_graph"]),
        ...mapListPanelMutations(["setSortKey"])
    }
})
</script>

<style lang="less" scoped>
@import 'listPanel.less';
</style>
