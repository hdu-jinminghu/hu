<template>
  <div class="flow_region">
    
    <!-- <div @click="save">
      保存
    </div> -->
    <div id="flowWrap" ref="flowWrap" class="flow-wrap" @drop="drop($event)" @dragover="allowDrop($event)">
      <div id="flow">
        <div v-show="auxiliaryLine.isShowXLine" class="auxiliary-line-x" :style="{width: auxiliaryLinePos.width, top:auxiliaryLinePos.y + 'px', left: auxiliaryLinePos.offsetX + 'px'}"></div>
        <div v-show="auxiliaryLine.isShowYLine" class="auxiliary-line-y" :style="{height: auxiliaryLinePos.height, left:auxiliaryLinePos.x + 'px', top: auxiliaryLinePos.offsetY + 'px'}"></div>
        <flowNode v-for="item in data.nodeList" :id="item.id" :key="item.id" :node="item" @setNodeName="setNodeName" @deleteNode = "deleteNode" @changeLineState="changeLineState" @showInfo="showInfo" @changInfo="changInfo"></flowNode>
        <brush ref="brush" :deActiveTag="deActiveTag"></brush>
      </div>
      <div :class="['draftButton']">
        <el-button type="info" icon="el-icon-refresh-right" circle @click="adjustLayout"></el-button>
        <el-button type="danger" icon="el-icon-delete" circle @click="cancelConnect"></el-button>
        <el-button type="success" icon="el-icon-check" circle @click="dialogFormVisibleModule=true"></el-button>
        <el-button type="primary" icon="el-icon-video-play" circle @click="dialogFormVisibleModel=true"></el-button>
      </div>
      <div :class="['config']">
        <!-- 损失函数数选择 -->
        <div :class="['lossConfig']">
          <el-select v-model="lossFc" placeholder="请选择">
            <el-option
              v-for="item in lossFcs"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </div>
        <!-- 数据集选择 -->
        <div :class="['datasetConfig']">
          <el-select v-model="dataset" placeholder="请选择">
            <el-option
              v-for="item in datasets"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </div>
      </div>
    </div>
    <div class="nodes-wrap">
      <div v-for="item in nodeTypeList" :key="item.type" class="node" draggable="true" @dragstart="drag($event, item)" @dragend="dragend($event, item)" >
        <div class="name">{{item.typeName}}</div>
      </div>
      <div  class="node" @click="changeMode" >
        <div :class="brushButtonStyle">brush</div>
      </div>
      <div :class="['divider']">
          <div :class="['divider__text']">
              modules
          </div>
      </div>
      <div v-for="item in Object.keys(graph)" :key="graph[item].type" class="node" draggable="true" @dragstart="drag($event, graph[item])" @dblclick="reload(graph[item])">
          <div class="name">{{item}}</div>
      </div>
    </div>
    <listPanel :class="['listPanel']"></listPanel>
    <!-- 设置属性 -->
    <el-dialog title="Attrs" :visible.sync="dialogFormVisible">
        <el-form :model="currentNode">
            <span>type:{{eventTarget}}</span>
            <template v-for="attr in Object.keys(currentNode)">
                <el-form-item :label="attr" :label-width="formLabelWidth" :key="attr">
                    <el-input v-model="currentNode[attr]"></el-input>
                </el-form-item>
            </template>
        </el-form>
        <div slot="footer" class="dialog-footer">
            
            <el-button @click="dialogFormVisible = false">Cancel</el-button>
            <el-button type="primary" @click="confirm(currentNode)">Ok</el-button>
        </div>
    </el-dialog>
    <!-- 保存模块 -->
    <el-dialog title="" :visible.sync="dialogFormVisibleModule">
        <el-form >
                <el-form-item label="Saved as" :label-width="formLabelWidth">
                    <el-input v-model="title"></el-input>
                </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisibleModule = false">Cancel</el-button>
            <el-button type="primary" @click="confirmModule()">Ok</el-button>
        </div>
    </el-dialog>
    <!-- 保存模型 -->
    <el-dialog title="" :visible.sync="dialogFormVisibleModel">
        <el-form >
                <el-form-item label="Model name" :label-width="formLabelWidth">
                    <el-input v-model="modelName"></el-input>
                </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisibleModel = false">Cancel</el-button>
            <el-button type="primary" @click="gModel()">Ok</el-button>
        </div>
    </el-dialog>
  </div>
</template>

<script>
import { jsPlumb } from "jsplumb"
// import { jsPlumb } from "@/utils/jsplumb"
// import { jsPlumb } from '../../../../utils/jsplumb'
import { nodeTypeList,lossFcs,datasets,formConfig} from './utils/init'
import { jsplumbSetting, jsplumbConnectOptions, jsplumbSourceOptions, jsplumbTargetOptions } from './utils/defaultConfig'
import { jsplumbSettingAdjust, jsplumbConnectOptionsAdjust, jsplumbSourceOptionsAdjust, jsplumbTargetOptionsAdjust } from './utils/adjustConfig'
import methods from "./utils/methods"
import data from "./utils/data.json"
import flowNode from "./node-item"
import brush from "./brush"
import ElementUI from 'element-ui'
import { createNamespacedHelpers } from 'vuex'
import listPanel from '../listPanel/listPanel.vue'
const { mapActions: mapLayoutActions,mapGetters:mapLayoutGetters,mapMutations: mapLayoutMutations,} = createNamespacedHelpers('layout')
const {  mapMutations: mapEditorMutations,mapGetters:mapEditorGetters} = createNamespacedHelpers('editor')
export default {
  name: "FlowEdit",
  components: {
    flowNode,
    brush,
    listPanel
  },
  data() {
    return {
      deActiveTag:true,
      dialogFormVisibleModel:false,
      modelName:'',
      title:"",
      eventTarget:undefined,
      currentNode:{},
      dialogFormVisible:false,
      dialogFormVisibleModule:false,
      jsPlumb: null,
      currentItem: null,
      nodeTypeList: nodeTypeList,
      lossFcs:lossFcs,
      datasets:datasets,
      lossFc:"CrossEntropyLoss",
      dataset:"CIFAR10",
      nodeTypeObj: {},
      data: {
        nodeList: [],
        lineList: []
      },
      modules: [],
      selectedList: [],

      jsplumbSetting: jsplumbSetting,
      jsplumbConnectOptions: jsplumbConnectOptions,
      jsplumbSourceOptions: jsplumbSourceOptions,
      jsplumbTargetOptions: jsplumbTargetOptions,

      jsplumbSettingAdjust:jsplumbSettingAdjust,
      jsplumbConnectOptionsAdjust:jsplumbConnectOptionsAdjust,
      jsplumbSourceOptionsAdjust:jsplumbSourceOptionsAdjust,
      jsplumbTargetOptionsAdjust:jsplumbTargetOptionsAdjust,

      jsplumbSettingDefault: jsplumbSetting,
      jsplumbConnectOptionsDefault: jsplumbConnectOptions,
      jsplumbSourceOptionsDefault: jsplumbSourceOptions,
      jsplumbTargetOptionsDefault: jsplumbTargetOptions,

      auxiliaryLine: { isShowXLine: false, isShowYLine: false},  //对齐辅助线是否显示
      auxiliaryLinePos: { width: '100%', height: '100%', offsetX: 0, offsetY: 0, x: 20, y: 20 },
      commonGrid: [5, 5], //节点移动最小距离
      selectModuleFlag: false, //多选标识
      rectAngle: {
        px: '',  //多选框绘制时的起始点横坐标
        py: '',  //多选框绘制时的起始点纵坐标
        left: 0,
        top: 0,
        height: 0,
        width: 0
      },
      form: formConfig,
      formLabelWidth: '120px',
      graph:{},
      modelName:'test',
      brushButtonStyle:{
        "name":true,
        "brushButtonActive":false
      }
    };
  },
  mounted() {
    this.jsPlumb = jsPlumb.getInstance();
    this.initNodeTypeObj()
    this.initNode()
    this.fixNodesPosition()
    this.$nextTick(() => {
      this.init();
    });
    this.$nextTick(()=>{
      this.draggableNode("editBrush")
    })
  },
  computed:{
    ...mapLayoutGetters(['getModelGraphList','getModelName']),
    ...mapEditorGetters(["getGraph"])
  },
  watch:{
    dataset:{
      immediate:true,
      handler(val){
        this.$nextTick(()=>{
          this.set_dataset(val)
        })
      }
    },
    getModelName:{
      immediate:true,
      handler(val){
        if(val == this.modelName){
          return
        }
        let data = JSON.parse(JSON.stringify(this.getModelGraphList[val]["sData"]))
        this.lossFc = this.getModelGraphList[val]["lossFc"]
        this.dataset = this.getModelGraphList[val]["dataset"]
        this.$nextTick(()=>{
          this.reload(data)
        })
        this.modelName = val
      }
    },
    getGraph:{
      handler(val){
        this.$nextTick(()=>{
          this.reload(val)
        })
      }
    }
  },
  methods: {
    ...methods,
    ...mapEditorMutations([
          "set_dataset"
      ]),
    ...mapLayoutActions([
          'genereModel',
        ]),
    ...mapLayoutMutations([
          'setModelSData',
        ]),
    initNodeTypeObj() {
      nodeTypeList.map(v => {
        this.nodeTypeObj[v.type] = v
      })
    },
    initNode() {
      this.data.lineList = data.lineList
      data.nodeList.map(v => {
        v.logImg = this.nodeTypeObj[v.type].logImg
        v.log_bg_color = this.nodeTypeObj[v.type].log_bg_color
        this.data.nodeList.push(v)
      })
    },
    dragend(e,item){
      this.eventTarget = item.typeName
      this.currentNode = JSON.parse(JSON.stringify(this.form[this.eventTarget]))
      this.$nextTick(()=>{
        this.dialogFormVisible = true
      })
    },
    saveFlow(){
      console.log(this.data)
    },
    dropFlow(){
        console.log(this.data)
    },
    confirm:function(layer){
        this.dialogFormVisible = false;
        let length = this.data["nodeList"].length
        this.data["nodeList"][length-1]["attrs"] = this.currentNode
        // let newLayer = {}
        // newLayer["attr"] = JSON.parse(JSON.stringify(layer));
        // newLayer["uid"] = this.uid;
        // newLayer["inputs"] = [];
        // newLayer["outputs"] = [];
        // newLayer["type"] = this.eventTarget;
        // newLayer["moduleId"] = this.eventTarget;
        // this.graph.push(newLayer);
    },
    confirmModule:function(){
      if(this.deActiveTag){
        let newGraph = {}
        newGraph["nodeList"] = JSON.parse(JSON.stringify(this.data["nodeList"]))
        newGraph["lineList"] = JSON.parse(JSON.stringify(this.data["lineList"]))
        newGraph['type'] = `module_${this.title}`
        newGraph['typeName'] = this.title
        newGraph['nodeName'] = this.title
        newGraph['log_bg_color'] = 'rgba(250, 205, 81, 0.2)'
        console.log(newGraph)
        this.graph[this.title] = newGraph
        this.dialogFormVisibleModule = false
      } else {
        this.brushModule()
      }
    },
    confirmModel:function(){
      console.log(this.modelName)
    },
    changInfo:function(node){
        this.currentNode = node["attrs"];
        this.$nextTick(()=>{
            this.dialogFormVisible = true
        })
    },
    gPartModel:function(graph,io,module,moduleList,nodeList,lineList,prefix){
      io[prefix] = {}
      // 构建节点
        for(let node of nodeList){
            let id = `${prefix}-${node["id"]}`
            if(prefix == ""){
              id = node["id"]
            }
            // 记录模块的io
            if(node["type"] == "input"){
                io[prefix]["input"] = id
            }
            else if(node["type"] == "output"){
                io[prefix]['output'] = id
            }
            // 记录模块 
            else if(node["type"].startsWith("module")){
              module[id] = node["typeName"]
              moduleList.push(id)
            }

            let node_ = {}
            node_["inputs"] = []
            node_["outputs"] = []
            node_["type"] = node["typeName"]
            node_["moduleId"] = `${prefix.replace(/-/g,"/")}/${node["nodeName"]}`
            node_["attr"] = node["attrs"]
            node_["uid"] = node["id"]
            graph[id] = node_
        }
      // 构建连接
        for(let line of lineList){
          if(prefix == ""){
            graph[`${line["from"]}`]["outputs"].push(`${line["to"]}`)
            graph[`${line["to"]}`]["inputs"].push(`${line["from"]}`)
          }
          else{
            graph[`${prefix}-${line["from"]}`]["outputs"].push(`${prefix}-${line["to"]}`)
            graph[`${prefix}-${line["to"]}`]["inputs"].push(`${prefix}-${line["from"]}`)
          }
        }
    },
    // io映射
    ioReplace:function(graph,io){
      for(let i in io){
        io[i]["input"] = graph[io[i]["input"]]["outputs"][0]
        io[i]["output"] = graph[io[i]["output"]]["inputs"][0]
      }
    },
    // 替换io节点，模块节点
    processG:function(graph,io){
      let nodeList = Object.keys(graph)
      let moduleId = Object.keys(io)
      function deep(nodeId,type){
        if(moduleId.indexOf(nodeId)>=0){
          console.log(nodeId)
          return deep(io[nodeId][type],type)
        } else {
          return nodeId
        }
      }

      for(let nodeId of nodeList){ 
        let node = graph[nodeId]
        // 处理io节点
        if(node["type"] == "input" || node["type"] == "output"){
          for(let input of node["inputs"]){
            graph[input]["outputs"].splice(0,1)
          }
          for(let output of node["outputs"]){
            graph[output]["inputs"].splice(0,1)
          }
          delete graph[nodeId]
          continue
        }
        // 处理模块节点
        if(Object.keys(this.form).indexOf(node["type"]) < 0){
          let input = node["inputs"][0]
          let indexI = graph[input]["outputs"].indexOf(nodeId)
          let output = node["outputs"][0]
          let indexO = graph[output]["inputs"].indexOf(nodeId)
          graph[deep(input,"input")]["outputs"].splice(indexI,1,deep(nodeId,"input"))
          graph[deep(output,"output")]["inputs"].splice(indexO,1,deep(nodeId,"output"))
          graph[deep(nodeId,"input")]["inputs"].push(input)
          graph[deep(nodeId,"output")]["outputs"].push(output)
          delete graph[nodeId]
        }

      }
    },
    gModel:function(){
        let graph = {}
        let io = {}
        let module = {} // 模块类型
        let moduleList = [] // 模块名
        this.gPartModel(graph,io,module,moduleList,this.data.nodeList,this.data.lineList,'')
        while(moduleList.length>0){
          let data = this.graph[module[moduleList[0]]]
          this.gPartModel(graph,io,module,moduleList,data["nodeList"],data["lineList"],moduleList[0])
          moduleList.splice(0,1)
        }

        this.ioReplace(graph,io)
        this.processG(graph,io)
        this.$nextTick(()=>{this.setModelSData([this.modelName,this.data,this.lossFc,this.dataset])})
        this.$nextTick(()=>{this.genereModel({"modelTxt":graph,"lossFc":this.lossFc,"dataset":this.dataset,"tolModule":this.graph,"g":"generator"})})
        this.$nextTick(()=>{this.dialogFormVisibleModel = false})
    },
    brushModule(){
      let {x,y,width,height} = this.$refs.brush.getBrushWH()
      let newGraph = {}
      let data = this.findAllNodes([x,y],[x+width,y+height])
      newGraph["nodeList"] = JSON.parse(JSON.stringify(data["nodeList"]))
      newGraph["lineList"] = JSON.parse(JSON.stringify(data["lineList"]))
      newGraph['type'] = `module_${this.title}`
      newGraph['typeName'] = this.title
      newGraph['nodeName'] = this.title
      newGraph['log_bg_color'] = 'rgba(250, 205, 81, 0.2)'
      this.graph[this.title] = newGraph
      this.dialogFormVisibleModule = false
    },
    changeMode(){
      this.deActiveTag = !this.deActiveTag
      this.brushButtonStyle["brushButtonActive"] = !this.brushButtonStyle["brushButtonActive"]
    },
  }
};
</script>

<style lang="less" scoped>
.flow_region {
  display: flex;
  width:calc( 100% - 10px);
  height: calc( 100% - 10px);
  margin: 5px;
  border: 1px solid #ccc;
  .nodes-wrap {
    width: 150px;
    height: 100%;
    border: 1px solid black;
    overflow-y: auto;
    .node {
      display: flex;
      height: 40px;
      width: 80%;
      margin: 5px auto;
      border: 1px solid #ccc;
      line-height: 40px;
      &:hover{
        cursor: grab;
      }
      &:active{
        cursor: grabbing;
      }
      .log {
        width: 40px;
        height: 40px;
      }
      .name {
        width: 0;
        flex-grow: 1;
      }
    }
  }
  .flow-wrap {
    border: 1px solid black;
    height: 100%;
    position: relative;
    overflow: hidden;
    outline: none !important;
    flex-grow: 1;
    background-image: url("../../../../assets/point.png");
    #flow {
      position: relative;
      width: 100%;
      height: 100%;
      
      .auxiliary-line-x {
        position: absolute;
        border: .5px dashed #2ab1e8;
        z-index: 9999;
      }
      .auxiliary-line-y {
        position: absolute;
        border: .5px dashed #2ab1e8;
        z-index: 9999;
      }
    }
  }
}
.divider{
    position: relative;
    margin: 15px 0;
    width:100%;
    height: 1px;
    background-image: linear-gradient(to right, black, gray);
}
.divider__text{
    left: 20px;
    transform: translateY(-50%);
    padding: 0 10px;
    background-color:rgb(238, 238, 238);
    font-size:14px;
    font-weight:500;
    position: absolute;
}
.listPanel{
  position: absolute;
  left: 7px;
  bottom: 7px;
  height: 400px;
  width: 400px;
  background-color: #2ab1e8;
}
.config {
  position: absolute;
  top: 0%;
  right: 0%;
}
</style>

<style lang="less">
.jtk-connector.active{
  z-index: 9999;
  path {
    stroke: #150042;
    stroke-width: 1.5;
    animation: ring;
    animation-duration: 3s;
    animation-timing-function: linear;
    animation-iteration-count: infinite;
    stroke-dasharray: 5;
  }
}
@keyframes ring {
  from {
    stroke-dashoffset: 50;
  }
  to {
    stroke-dashoffset: 0;
  }
}
.draftButton {
    position: absolute;
    bottom: 0%;
    right: 0%;
}

.brushButtonActive{
  box-shadow: 0 0 3px 1px;
}
</style>