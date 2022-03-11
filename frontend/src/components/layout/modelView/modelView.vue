<template>
    <div id="flowWrap" ref="flowWrap" class="flow-wrap" 
        @drop="drop($event)" 
        @mousedown="setInitMousePos($event)" 
        @mouseup="releaseMouse($event)" 
        @dragover="allowDrop($event)" 
        @mousemove="getMousePos($event)" 
        @keydown="setEnv($event)" 
        @keyup="releaseEnv($event)">

      <div :class="['model-view-explore-stage']">{{stage}}</div>
      <div :class="['model-view-overNodeId']">{{overNodeId}}</div>
      <div :class="['model-view-back']" @click="backstep()"></div>
      <div id="flow">
        <div v-show="auxiliaryLine.isShowXLine" class="auxiliary-line-x" :style="{width: auxiliaryLinePos.width, top:auxiliaryLinePos.y + 'px', left: auxiliaryLinePos.offsetX + 'px'}"></div>
        <div v-show="auxiliaryLine.isShowYLine" class="auxiliary-line-y" :style="{height: auxiliaryLinePos.height, left:auxiliaryLinePos.x + 'px', top: auxiliaryLinePos.offsetY + 'px'}"></div>
        <flowNode v-for="item in graph.nodeList" :id="item.id" :key="item.id" :node="item" @setNodeName="setNodeName" @deleteNode = "deleteNode" 
        @changeLineState="changeLineState" @showInfo="showInfo" @mouseOver="nodeMouseOver" @changInfo="changInfo" @explore="explore" @targetLayer="targetLayer" @batchChannel="channelsDialogFormVisible=true"></flowNode>
        <div :class="['brush']"></div>
      </div>
      <el-button type="info" icon="el-icon-refresh-right" circle @click="adjustLayout" :class="['refresh-right-button']"></el-button>


        <el-dialog title="参数设置" :visible.sync="dialogFormVisible">
            <el-form :model="autoConfig">
                <el-form-item label="epoch" :label-width="formLabelWidth">
                <el-input v-model="autoConfig.epoch" autocomplete="off"></el-input>
                </el-form-item>

                <!-- <el-form-item label="depth" :label-width="formLabelWidth">
                <el-input v-model="autoConfig.depth" autocomplete="off"></el-input>
                </el-form-item> -->

                
                <el-form-item label="acc" :label-width="formLabelWidth">
                <el-input v-model="autoConfig.acc" autocomplete="off"></el-input>
                </el-form-item>

                <el-form-item label="loss" :label-width="formLabelWidth">
                <el-input v-model="autoConfig.loss" autocomplete="off"></el-input>
                </el-form-item>

                <el-form-item label="tol" :label-width="formLabelWidth">
                <el-input v-model="autoConfig.tol" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogFormVisibleOk()">确 定</el-button>
            </div>
        </el-dialog>

        <el-dialog :visible.sync="duplicateDialogFormVisible">
            <el-form>
                <el-form-item label="duplicate" :label-width="formLabelWidth">
                <el-input v-model="duplicateTimes" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="duplicateDialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="dupliacteOk()">确 定</el-button>
            </div>
        </el-dialog>

        <el-dialog :visible.sync="channelsDialogFormVisible">
            <el-form>
                <el-form-item label="channels" :label-width="formLabelWidth">
                <el-input v-model="channels" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="channelsDialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="channelsDialogFormVisibleOk()">确 定</el-button>
            </div>
        </el-dialog>

    </div>
</template>

<script>
import utils from '@/utils/layout'
import methods from './modelView.method'
import gMethod from './gModel.method'
import flowNode from "./nodeItem/nodeItem"
import {vgg16,resnet50,googlenet,Alexnet,Lenet} from '@/components/build/template'
import {jsplumbSetting,jsplumbConnectOptions,jsplumbSourceOptions,jsplumbTargetOptions} from './jsPlumbConfig';
import { nodeTypeList,lossFcs,datasets,formConfig} from './init'
import { createNamespacedHelpers } from 'vuex'
const {mapGetters:mapModelViewGetters,mapMutations:mapModelViewMutations,mapActions:mapModelViewActions} = createNamespacedHelpers('modelView')
const {mapGetters:mapListPanelGetters} = createNamespacedHelpers('listPanel')
const {mapGetters: mapDebugGetters} = createNamespacedHelpers('debug')
const {mapMutations:mapIndicatorMutations} = createNamespacedHelpers('indicator')
export default {
    components:{
        flowNode
    },
    data(){
        return {
            channelsDialogFormVisible:false,
            duplicateDialogFormVisible:false,
            duplicateTimes:0,
            channels:0,
            env:{"ctrl":false,"click":false,"KeyV":false},
            jsPlumb:null,
            auxiliaryLinePos:{ width: '100%', height: '100%', offsetX: 0, offsetY: 0, x: 20, y: 20 },
            auxiliaryLine:{ isShowXLine: false, isShowYLine: false},
            graph:{'nodeList':[],'lineList':[]},
            jsplumbSetting:jsplumbSetting,
            jsplumbConnectOptions:jsplumbConnectOptions,
            jsplumbSourceOptions:jsplumbSourceOptions,
            jsplumbTargetOptions:jsplumbTargetOptions,
            moduleList:{},
            form:formConfig,
            lossFc:'CrossEntropyLoss',
            dataset:'CIFAR10',
            modelName:'test',
            exploreStage:[],
            stages:['graph'],
            stage:'',
            selectedItem:[],
            autoConfig: {
                epoch: undefined,
                // acc: undefined,
                // loss: undefined,
                depth: undefined,
                tol:undefined
            },
            dialogFormVisible:false,
            formLabelWidth: '120px',
            duplicateOp:1,
            overNodeId:""
        }
    },
    filters:{
        stageConnect(val){
            return val.join('/')
        }
    },
    mounted(){
        this.jsPlumb = jsPlumb.getInstance();
        this.init()
        let modules = {...vgg16,...resnet50,...googlenet,...Alexnet,...Lenet}
        let resModules = Object.keys(resnet50)
        let vggModules = Object.keys(vgg16)
        let googlenetModules = Object.keys(googlenet)
        let AlexnetModules = Object.keys(Alexnet)
        let LetnetModules = Object.keys(Lenet)
        this.initModule(modules)
        this.setModuleCategory([resModules,vggModules,googlenetModules,AlexnetModules,LetnetModules])
    },
    computed:{
        ...mapModelViewGetters(['getDragIem','getDir','getModulId','getModuleList','getActiveModule','getGraph']),
        ...mapListPanelGetters(['getAutomlGraph']),
        ...mapDebugGetters(['getDebugDir'])
    },
    watch:{
        getGraph:{
            handler(val){
                this.exploreStage.splice(0,this.exploreStage.length)
                let exploreStage = []
                let stages = JSON.parse(JSON.stringify(this.stages))
                let current = val
                if(val != undefined){
                    for(let i of this.stages){
                        if(i == "graph"){
                            exploreStage.push(current)
                        } else {
                            for(let vertex of current["nodeList"]){
                                if(i == vertex["id"]){
                                    current = vertex
                                    break
                                }
                            }
                        }
                    }
                }
                utils.layout(current);
                this.reload(current);
                // this.$nextTick(()=>{
                //     this.exploreStage = exploreStage
                //     this.stages = stages
                // })
                setTimeout(()=>{
                    this.exploreStage = exploreStage
                    this.stages = stages
                },0)
            }
        },
        env:{
            deep:true,
            handler(val){
                (val["click"] && val["ctrl"]) || (this.setSelected());
                (val["KeyV"] && val["ctrl"]) && (this.duplicateDialogFormVisible = true);
            }
        },
        stages:{
            immediate:true,
            handler(val){
                this.stage = val.join('/')
                this.$nextTick(()=>{
                    this.setGlobalStage(this.stage)
                })
            }
        },
        getActiveModule:{
            immediate:true,
            handler(val){
                val && (function(that){
                    let graph = JSON.parse(JSON.stringify(val));
                    utils.layout(graph);
                    that.reload(graph)
                    that.setActiveModule('')
                })(this)
            }
        },
        getDragIem:{
            immediate:true,
            handler(val){
                this.currentItem = val
            }
        },
        getDir:{
            immediate:true,
            handler(val){
                this.moduleList = this.getModuleList
                val == 'clear' && this.cancelConnect()
                val == 'confirm' && this.setModule()
                val == 'run' && this.gModel()
                val == 'search' && (this.dialogFormVisible = true)
                // this.postAutoMlRough()
                val == 'info' && (console.log(this.graph))
                this.$nextTick(()=>{this.setDir('')})
            }
        },
        getAutomlGraph:{
            immediate:true,
            handler(val){
                val && (function(that){
                that.reload(val)})(this)
            }
        },
        getDebugDir:{
            immediate:true,
            handler(val){
                val == 'continue' && (function(that){
                    let graph = that.graph
                    if(that.exploreStage.length > 0){
                        graph = that.exploreStage[0]
                    }
                    that.$nextTick(()=>{that.genereModel({"modelTxt":graph,"lossFc":that.lossFc,"dataset":that.dataset,"g":"continue"})})
                })(this)
            }
        },
        // dialogFormVisible:{
        //     immediate:true,
        //     handler(val){
        //         if(!val){
        //             this.autoConfig.epoch && ( this.autoConfig.acc || this.autoConfig.loss || this.autoConfig.tol ) && this.postAutoMlRough(this.autoConfig)
        //         }
        //     }
        // },
        // duplicateDialogFormVisible:{
        //     immediate:true,
        //     handler(val){
        //         if(!val && this.duplicateTimes>0){
        //             this.duplicate()
        //         }
        //     }
        // }
    },
    methods:{
        ...methods,
        ...gMethod,
        ...mapModelViewMutations(['changeItemInfo','setModelSData','setModuleData','setDir',
        'setActiveModule','initModule','setGlobalStage','setModuleCategory','setOriGraph',"setChannels"]),
        ...mapModelViewActions(['genereModel','roughAutoml']),
        ...mapIndicatorMutations(['set_prun_target','set_prun_targetVertex']),
        dupliacteOk:function(){
            this.duplicateDialogFormVisible = false;
            (this.duplicateTimes>0) && this.duplicate()
        },
        dialogFormVisibleOk:function(){
            this.dialogFormVisible = false;
            this.autoConfig.epoch && ( this.autoConfig.acc || this.autoConfig.loss || this.autoConfig.tol ) && this.postAutoMlRough(this.autoConfig)
        },
        channelsDialogFormVisibleOk:function(){
            this.channelsDialogFormVisible = false;
            (this.channels>0) && this.setChannels(this.channels)
        }
    }
}
</script>

<style lang="less" scoped>
@import 'modelView.less';
</style>