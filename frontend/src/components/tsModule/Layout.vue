
<template>
  <div style="height:100%;width:100%">
    <div class="temp" style="height:100%;width:100%">
      <!-- 可从这里加入你们的组件 -->
      <div id="header" :class="['header']">
        <div class='title'>Title</div>
        <div class='header button_select'>
          <el-select v-model="modelName" placeholder="请选择">
            <el-option
              v-for="item in modelList"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </div>
        <div class="header button_right" @click="editModel">edit</div>
      </div>
      <div style="display:flex;flex-direction:row;width:100%;height:calc( 100% - 69px)" :class="editPage?'editPage close':'editPage open'">
        <div id="mainContent" :class="['mainStyle']">
          <div id="GraphView" class="GraphView" :style="{width:graphStyle.width,height:graphStyle.height}">
            <div class="controlParam">
              <div id="monitor" style="display:flex;flex-direction:row">
                  <span>Monitor:</span>
                  <el-cascader
                    ref="cascader"
                    v-model="value"
                    :options="options"
                    :props="{}"
                    @change="test(value)">
                      <template slot-scope="{ node, data }">
                        <span>{{ data.label }}</span>
                        <span v-if="node.isLeaf"> 
                          <i class="el-icon-delete" @mousedown="delOption(node)"></i> 
                        </span>
                      </template>
                  </el-cascader>
                </div>
                <div style="display:flex;flex-direction:row">
                  <span>Frequence:</span>
                  <el-input v-model="cycle" placeholder="" @change="setFrequence_()"></el-input>
                  <span>Lr:</span>
                  <el-input v-model="lr" placeholder="" @change="setLr_()"></el-input>
                  <span>Batch:</span>
                  <el-input v-model="batch" placeholder="" @change="setBatch_()"></el-input>
                  <span>Epoch:</span>
                  <el-input v-model="epoch" placeholder="" @change="setEpoch_()"></el-input>
                  <div class="controlButton">
                    <el-button type="info" @click="historyMenu('Saved')">Save</el-button>
                    <el-button type="info" v-if="play" @click="changeState">Stop</el-button>
                    <el-button type="info" v-if="!play" @click="changeState">Run</el-button>
                  </div>
                </div>
              
            </div>
            <div id="Graph" class="Graph">
              <svg id="svg-canvas" style="height:100%;width:100%" >
                <defs>
                  <marker
                    id="dot"
                    markerUnits="strokeWidth"
                    markerWidth="10"
                    markerHeight="10"
                    viewBox="0 0 20 20"
                    refX="10"
                    refY="10"
                  >
                    <circle
                      cx="10"
                      cy="10"
                      r="4"
                      style="fill: black;"
                    />
                  </marker>
                </defs>
                <g id="draw" style="height:100%;width:100%" />
              </svg>
            </div>
            <aside id="annotationMain">
              <div style="font-size:3px">
                <div id="Conv"/>
                <div id="Relu"/>
                <div id="BatchNorm"/>
                <div id="Dropout"/>
                <div id="Others"/>
              </div>
            </aside>
          </div>
          
        
        <div id="footer" class="footerStyle">
          <el-col :span="12" :key="'scalar'">
            <div id="scalarView" class="scalarView">
              <div id="scalarHeader" class="scalarHeader">
                Traning
              </div>
              <div id="scalarContent" class="scalarContent">
                <div id="controlPanel" class="controlPanel">
                  <el-tabs v-model="activeName" type="border-card">
                    <el-tab-pane v-for="item in Tabs" :key="item.name" :label="item.label" :name="item.name">
                      </el-tab-pane>
                  </el-tabs>
                </div>
                <div id="content" class="content">
                  <template>
                    <scalar 
                      v-show="div_global=='ac'"
                      :height="scalarHeight"
                      :width="scalarWidth"
                      :editPage="editPage"
                    ></scalar>
                    <compare 
                      v-show="div_global=='compare'"
                      :compareData="compareData"
                      :height="scalarHeight"
                      :width="scalarWidth"
                    ></compare>
                    <paramMatrix
                        v-show="div_global=='param'"
                        :tackle_node="tackle_node"
                        :isShow="monitorTag"
                        :n_activate_tag="activeName"
                      >
                    </paramMatrix>
                  </template>
                </div>
              </div>
            </div>
          </el-col>

          <el-col :span="12" :key="'indicator'">
            <div id="indicatorView" class="indicatorView">
              <div id="indicatorHeader" class="indicatorHeader">
                  Indicator
              </div>
              <div id="indicatorContent" class="indicatorContent">
              <template>
                <indicator
                  :height="scalarHeight"
                  :width="indicateWidth"
                  :isShow="div_global=='param'"
                  v-on:opContent="setOpContent"
                >
                </indicator>
              </template>
              </div>
            </div>
            </el-col>
        </div>
        </div>
        <aside class="section-right">
          
          <div id="History" :class="historyStyle">
                <div id="HistoryHead" class="HistoryHead"> History
                </div>
                <div id="HistoryContent" class="HistoryContent">
                  <svg id="history" style="height:100%;width:100%;float:left">
                    
                    <g id="nodes"/>
                    <g id="edges"/>
                  <defs>
                      <marker id="markerArrow" markerUnits="strokeWidth" markerWidth="12" markerHeight="12" viewBox="0 0 12 12" refX="6"
                          refY="6" orient="auto">
                          <path d="M2,2 L10,6 L2,10 L2,2" style="fill: #67C23A;" />
                      </marker>
                      <linearGradient id="savedLinear" x1="0%" y1="0%" x2="0%" y2="100%"> <stop offset="30%" stop-color="#ffffff"/> <stop offset="100%" stop-color="rgb(103, 194, 58)"/> </linearGradient>
                      <linearGradient id="notSavedLinear" x1="0%" y1="0%" x2="0%" y2="100%"> <stop offset="30%" stop-color="#ffffff"/> <stop offset="100%" stop-color="#EB6100"/> </linearGradient>
                  </defs>
                  <defs>
                    <filter id="blur-2px" x="-15%" y="-20%"  width="130%" height="140%">
                      <feGaussianBlur
                        in="SourceGraphic"
                        stdDeviation="10" />
                      <!-- <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="hsla(180,90%,40%,0.9)" /> -->
                    </filter>
                  </defs>
                  <defs>
                    <radialGradient id="grey_blue" cx="50%" cy="50%" r="50%"
                    fx="50%" fy="50%">
                      <stop offset="0%" style="stop-color:rgb(200,200,200);
                      stop-opacity:0"/>
                      <stop offset="100%" style="stop-color:rgb(0,0,255);
                      stop-opacity:1"/>
                    </radialGradient>
                  </defs>

                  <g id="draw" style="height:100%;width:100%" />
                </svg>
                </div>
                <aside style="height:100px">
                  <div>
                    <div id="Accuracy"/>
                    <div id="Loss"/>
                    <div id="Saved"/>
                    <div id="NotSaved"/>
                  </div>
                </aside>
            </div>
            <drawer :editPage="editPage" :class="drawerStyle"></drawer>
            <button class="panel-change" @click="changePanel()"></button>
        </aside>
    </div>
    <div class="editPage" :class="editPage?'editPage open':'editPage close'">
      <editComponent></editComponent>
    </div>
  </div>
  </div>
</template>

<script>
import { scalar, paramMatrix,indicator,compare,drawer} from './childComponent'
import {editComponent} from './childComponent/edit/index'
import * as d3 from 'd3'
import dagreD3 from 'dagre-d3/dist/dagre-d3'
import { createNamespacedHelpers } from 'vuex'
import $ from 'jquery'
import 'jquery-contextmenu'
import 'jquery-contextmenu/dist/jquery.contextMenu.css'
import methods from "./Layout.method"

const { mapActions: mapLayoutActions,mapState:mapLayoutStates,mapGetters:mapLayoutGetters,mapMutations: mapLayoutMutations,} = createNamespacedHelpers('layout')
const {mapGetters:mapScalarGetters} = createNamespacedHelpers('scalar')
const {mapMutations: mapIndicatorMutations,mapGetters:mapIndicatorGetters} = createNamespacedHelpers('indicator')

var titleHeight = 40 // 标题栏高度
var cornerR = 5// 圆角大小
var lineWidth = 1 // 边框线条宽度
var expandNode = []
var nodeInfo = []
var monitorable = ['_convolution','batch_norm','linear']

export default {
    name: 'HelloWorld',
    components: {
      scalar,paramMatrix,indicator,compare,editComponent,drawer
    },
    data () {
        return {
          modelName:'',
          editPage:true,
          opContent:"root",
          epoch:0,
          batch:0,
          lr:0,
          value:'',
          options: [],
          activeName:'ac',
          Tabs:[{"label":"acc/loss","name":"ac"}],
          cycle:0,
          saved:[],
          div_global:"ac",
          showTag:true,
          test_:0,
          graphRender:null,
          graphStyle:{
            width: "calc(100% -16px)",
            height:"calc(100% -16px)",
            border:"solid 1px black"
          },
          scalarHeight:0,
          scalarWidth:0,
          indicateWidth:0,
          indicate:{},
          tackle_node:'',
          urls:[],
          op:'',
          actiUrls:[],
          monitorTag:true,
          initTag:true,
          lastClicked: null, //  上一次点击
          expandTag: false,
          // node_:'',   //!  临时注释node
          // div_global_:true,  //!  临时注释
          history: [],
          play:true,
          historyData: {"uid":"t0-0-TRUE","label":"0","name":"0","tag":"TRUE","ancestor":"0","children":[]}, //编辑历史数据,ancestor实际为结构路径
          modelAmount:1,
          virNodeId:0,
          nowStatus:NaN,
          // historyData_:[
          //               [{"type":"Saved","id":"t0/1","acc":0.9,"compress":0.8,"parent":null,"pPos":null}],
          //               [{"type":"Saved","id":"t1/3","acc":0.7,"compress":0.6,"parent":"t0/1","pPos":[0,0]},{"type":"Saved","id":"t1/2","acc":0.7,"compress":0.6,"parent":"t0/1","pPos":[0,0]}],
          //               [{"type":"NotSaved","id":"t1/4","acc":0.7,"compress":0.6,"parent":"t1/3","pPos":[0,1]}],
          //               [{"type":"NotSaved","id":"t1/5","acc":0.7,"compress":0.6,"parent":"t1/4","pPos":[0,2]}],
          //               [{"type":"NotSaved","id":"t1/6","acc":0.7,"compress":0.6,"parent":"t1/5","pPos":[0,3]}],
          //             ]
          historyData_:[
            [{"id":"t0-0-Saved","label":"0","name":"0","ancestor":"0","pPos":null,"pos":[0,0],"acc":0,"loss":0,"parent":null,"type":"Saved","children":[],"content":"root"}],
          ],
          compareData:{},
          bank:["#EB6100","paleturquoise","purple","brown"],
          activate:[],
          historyDataList:{},
          historyStyle:{
            "History":true,
            "History-close":false
          },
          drawerStyle:{
            "History-close":true
          }

        }
    },
    computed:{
        ...mapLayoutStates(['categoryInfo','modelList',]),
        ...mapLayoutGetters(['getCompare','getBatch','getEpoch','getLr','getStructData','getKernelData',
            "getCycle","getMonitorList","getDataType",'getModelName','getTarget']),
        ...mapScalarGetters(["get_scalar_data"]),
        ...mapIndicatorGetters(["get_prun_tag"])
    },
    watch:{
        getTarget:{
          handler(val){
              var appendix = []
              if(this.getTarget["tag"]) {
                  var bn = "None"
                  if(this.getTarget["bn"]){
                      bn = this.getTarget["bn"]["t"]
                  }
                  var relu = "None"
                  if(this.getTarget["relu"]){
                      relu = this.getTarget["relu"]["t"]
                  }
                  var conv2 = "None"
                  if(this.getTarget["conv2"]){
                      var conv2 = this.getTarget["conv2"]["t"]
                  }

                  var linear = "None"
                  if(this.getTarget["linear"]){
                      var linear = this.getTarget["linear"]["t"]
                  }
                  appendix.push(bn)
                  appendix.push(relu)
                  appendix.push(conv2)
                  appendix.push(linear)
              }
              this.reset_finish_state()
              this.setInitData({"Id":this.tackle_node,"appendix":JSON.stringify(appendix)})
          }
        },
        getModelName:{
            immediate: true,
            handler(val){
                this.modelName = val
            }
        },
        modelName:function(val,oldval){
          this.selectModel(val)
          this.historyDataList[oldval] = {}
          this.historyDataList[oldval]["data"] = JSON.parse(JSON.stringify(this.historyData_))
          this.historyDataList[oldval]["modelAmount"] = this.modelAmount
          this.historyDataList[oldval]["virNodeId"] = this.virNodeId

          if(Object.keys(this.historyDataList).indexOf(val)>=0){
            this.historyData_ = this.historyDataList[val]["data"]
            this.modelAmount = this.historyDataList[val]["modelAmount"]
            this.virNodeId = this.historyDataList[val]["virNodeId"]
            this.nowStatus = this.historyData_[0][0]
            this.drawHistory()
          } else {
            this.historyData_ = [
            [{"id":"t0-0-Saved","label":"0","name":"0","ancestor":"0","pPos":null,"pos":[0,0],"acc":0,"loss":0,"parent":null,"type":"Saved","children":[],"content":"root"}],
          ]
            this.nowStatus = this.historyData_[0][0]
            this.modelAmount=1
            this.virNodeId=0
            this.drawHistory()
          }
          if(this.editPage == false){
            // 重新获取图和参数
            this.initFeatchData()
            this.rContorl()
            this.genereModel({"modelTxt":{},"lossFc":"","dataset":"","tolModule":{},"g":"reload"})
          } else {
            this.genereModel({"modelTxt":{},"lossFc":"","dataset":"","tolModule":{},"g":"reload"})
          }
          
        },
        getCompare:function(val) {
          let tag = true
          for(let i in this.Tabs){
            if(this.Tabs[i].name == "compare"){
              tag = false
              break
            }
          }
          console.log(val)
          if(Array.from(Object.keys(val)).length>0){  
            if(tag){
              this.Tabs.splice(1,0,{"label":"compare","name":"compare"})
            }
          } else{
            if(!tag){
              this.Tabs.splice(1,1)
              this.div_global = "ac"
            }
          }
          this.compareData = val
        },
        getDataType:function(val) {
          this.Tabs.splice(1,this.Tabs.length-1)
          this.activeName = "ac"
          for(var i=0;i<val.length;i+=1){
            this.Tabs.push({"label":`${val[i]}:current`,"name":`${val[i]}:current`})
            this.Tabs.push({"label":`${val[i]}:update`,"name":`${val[i]}:update`})
            this.Tabs.push({"label":`${val[i]}:contrast`,"name":`${val[i]}:contrast`})
          }
        },
        activeName:function(val) {
          if(val == "ac") {
            this.div_global = "ac"
          } else if (val == "compare"){
            this.div_global = "compare"
          } else {
            this.div_global = "param"
          }
        },
        getCycle:function(val) {
          this.cycle = parseInt(val)
        },
        getLr:function(val) {
          this.lr = parseFloat(val)
        },
        getBatch:function(val){
          this.batch = parseInt(val)
        },
        getEpoch:function(val){
          this.epoch = parseInt(val)
        },
        saved:function(val) {
          var res = []
          const idTransformer = this.idTransformer
          for(var i = 0; i<val.length; i+=1) {
            res.push(idTransformer(val[i].uid))
          }
          var list = JSON.stringify(res)
          this.monitor({"monitorList":list,"tag":"save"})
        },
        getKernelData:function(val){
          this.kernelData = val
          this.doubleNode()
        },
        getStructData:function(val){
          this.structData = val
          this.frameWork()
        },
        get_prun_tag:function(val){
          let self = this
          this.historyMenu(self.opContent)
        },
        editPage:function(val){
          if(val == false){
            this.initFeatchData()
            this.rContorl()
          }
        }
    },
    mounted(){
        this.scalarHeight = d3.select(".scalarContent").property("clientHeight") - 60
        this.scalarWidth = d3.select(".scalarContent").property("clientWidth")
        this.indicateWidth = d3.select(".indicatorContent").property("clientWidth")
        this.nowStatus = this.historyData_[0][0]
        
    },
    methods:{
        ...mapIndicatorMutations(["reset_finish_state"]),
        ...mapLayoutMutations([
          "setTargetNode",
          "setCompare",
          "selectModel"
        ]),
        ...mapLayoutActions([
          'initWaitingPage',
          'initFeatchData',
          'featchKernel',
          'rContorl',
          'cContorl',
          'monitor',
          'setCycle',
          'setLr',
          'setBatchsize',
          'setTrainCycle',
          'setPlayTag',
          "setKeepTag",
          "fetchTrainData",
          "genereModel",
          "setInitData"
        ]),
        ...methods,
        setOpContent:function(val){
          this.opContent = val
        },
        frameWork:function(){
          const self = this
          const frameWork = this.frameWork
          const nodeHold = this.nodeHold
          const data = this.structData
          const available = this.available
          const PosAdaption = this.PosAdaption
          const labelTransformer = this.labelTransformer
          const kernelData = this.kernelData
          const successor = this.successor
          const idTransformer = this.idTransformer
          const setTargetNode = this.setTargetNode
          var idTransformerFrontend = this.idTransformerFrontend
          
          var g = new dagreD3.graphlib.Graph({ compound: true })
            .setGraph({rankdir: "LR"}) //横向显示
            .setDefaultEdgeLabel(function() {
              return {}
            })

          data.forEach(function(v) {
            v.id = v.uid
            v.clicked = false
            if (v.label) {
              if (v.label.length > 9) {
                v['name'] = v.label
                v.label = v.label.slice(0, 8) + '...'
              }
            }
            if (available(v.uid)) {
              const uid_t = labelTransformer(v.uid)
              if(uid_t in kernelData){
                const detail = kernelData[uid_t]
                v.kernel = detail.shape
                v.op_ = detail.type
              }
              g.setNode(v.uid, v)
              v.targets.forEach(function(u) {
                if (available(u.id)) {
                  const edgeLabel = v.uid + '__' + u.id
                  g.setEdge(v.uid, u.id, { 'id': edgeLabel, 'label': u.info, curve: d3.curveBasis ,style: "fill:none;stroke:#333"})
                  nodeHold(v.uid, edgeLabel, u.id, 1, v.op, v.attrs)
                  nodeHold(u.id, edgeLabel, v.uid, 0, undefined, u.attrs)
                }
              })
              nodeHold(v.uid, '', '', 1, v.op, v.attrs)
            } else {
              v.clusterLabelPos = 'top'
              g.setNode(v.uid, v)
            }
          })
          for (let i = 0; i < expandNode.length; i++) {
            const sub = expandNode[i].sub_net
            sub.forEach(function(v) {
              v.id = v.uid
              if (v.label) {
                if (v.label.length > 9) {
                  v['name'] = v.label
                  v.label = v.label.slice(0, 8) + '...'
                }
              }
              g.setParent(v.uid, expandNode[i].uid)
              if (available(v.uid)) {
                const uid_t = labelTransformer(v.uid)
                if(uid_t in kernelData){
                  const detail = kernelData[uid_t]
                  v.kernel = detail.shape
                  v.op_ = detail.type
                }
                g.setNode(v.uid, v)
                v.targets.forEach(function(u) {
                  if (available(u.id)) {
                    const edgeLabel = v.uid + '__' + u.id
                    g.setEdge(v.uid, u.id, { 'id': edgeLabel, 'label': u.info, curve: d3.curveBasis,style: "fill:none;stroke:#333"})
                    nodeHold(v.uid, edgeLabel, u.id, 1, v.op, v.attrs)
                    nodeHold(u.id, edgeLabel, v.uid, 0, undefined)
                  }
                })
                nodeHold(v.uid, '', '', 1, v.op, v.attrs)
              } else {
                v.clusterLabelPos = 'top'
                g.setNode(v.uid, v)
              }
            })
          }
          g.nodes().forEach(function(v) {
            const node = g.node(v)
            if (node !== undefined) {
              node.rx = node.ry = 10 // 圆角半径
              node.width = 100 // 节点长度
              node.height = 50 //  节点宽度
              node.style = 'rx:12.5px' + ';ry:12.5px' + ';stroke-width:1px' + ';stroke:' + '#696969'
            }
          })
          const render = new dagreD3.render()

          const svg = d3.select('#svg-canvas')
          this.graphRender = g
          
          // 布局
          dagreD3.dagre.layout(g)
          // 以展开或缩小节点为基准修正坐标
          var offset_y = 0
          var offset_x = 0
          if(self.lastClicked){
            var v = self.lastClicked["id"]

            var core_x = g.node(v).x
            var core_y = g.node(v).y

            offset_y = core_y - self.lastClicked["core_y"]
            offset_x = core_x - self.lastClicked["core_x"]

            for(var i=0;i<g.edges().length;i+=1){
              var points = g.edge(g.edges()[i]).points
              for(var j=0;j<points.length;j+=1){
                points[j].y = points[j].y - offset_y
                points[j].x = points[j].x - offset_x
              }
            }
            for(var i=0;i<g.nodes().length;i+=1){
              var node = g.node(g.nodes()[i])
              node.y = node.y - offset_y
              node.x = node.x - offset_x

            }
          }


          
          self.expandTag = false
          render(d3.select('#svg-canvas g'), g)
          renderGraph()
          
          function renderGraph() {

            self.initPos()
            
            const zoom = d3.zoom().on('zoom', function() {
              d3.select('#svg-canvas g').attr('transform', d3.event.transform)
            })
            svg.call(zoom).on('dblclick.zoom', null)

            // 单击
            d3.selectAll('#svg-canvas .node').on('click', function(v) {
              const node = g.node(v)
              // console.log(node)
              const op = ["_convolution","batch_norm","linear","relu_"]
              if(op.indexOf(node.op) >= 0) {
                self.addSave(node)
              }
            })
            // 双击
            d3.selectAll('#svg-canvas .node').on('dblclick', function(v) {
              // var index = -1
              // 先判断点击节点在不在扩展节点中
              if (g.node(v).sub_net.length !== 0) {
                const names = v.split('/')
                const layer = names.length
                // 扩展后的节点没有子节点, 无法通过计算获取颜色值, 在重新绘制之前获取
                expandNode.push({
                  'uid': v,
                  'layer': layer,
                  'sub_net': g.node(v).sub_net,
                  'label': g.node(v).label,
                  // fill: fillCurrent
                })

                // bubbleSortExpand(expandNode)
                nodeInfo.splice(0, nodeInfo.length)

                
                var core_x = self.graphRender.node(v).x
                var core_y = self.graphRender.node(v).y
                self.expandTag = true
                self.lastClicked = {"id":v,"core_x":core_x,"core_y":core_y}
                frameWork(data)
                // 获取当前点击节点信息, 如果节点是最外层节点, 在 data 中查找, 否则在扩展节点中的 sub_net 中查找
                let currentNode = data.find(item => item.uid === v)

                if (!currentNode && expandNode && expandNode.length) {
                  // eslint-disable-next-line no-labels
                  loopExpandNode:
                  for (const expand of expandNode) {
                    for (const sub of expand.sub_net) {
                      if (sub.uid === v) {
                        currentNode = sub
                        // eslint-disable-next-line no-labels
                        break loopExpandNode
                      }
                    }
                  }
                }
                PosAdaption(currentNode);
              } else {
                self.play = false
                const node = g.node(v)
                self.tackle_node = idTransformer(v)
                self.monitorTag = self.monitorTag? false:true
                if(node.op == "_convolution") {
                  
                  const u = idTransformer(v)
                  var success = {}
                  successor(v,success)
                  success["conv1"] = {"r":v,"t":idTransformer(v)}
                  setTargetNode(success)
                }
              }
            })

            d3.selectAll('#svg-canvas .cluster').style('fill-opacity', '0.55').attr('font-weight', '600').on('dblclick', function(v) {
            const indexRecord = []
            const names = v.split('/')
            const namesLength = names.length
            
            var expandNode_before = []

            for(let i=0;i<expandNode.length;i+=1) {
              expandNode_before.push(expandNode[i].uid)
            }

            // var dropCluster = []  //  保存要丢弃的cluster
            // 遍历扩展结点
            for (let i = expandNode.length - 1; i >= 0; i--) {
              const uid = expandNode[i].uid
              const uids = uid.split('/')
              const uidLength = uids.length
              // 查找以改名为前缀的节点
              if (uidLength >= namesLength) {
                if (uids.slice(0, namesLength).join('/') === v) {
                  indexRecord.push(i)
                }
              }
              for (let j = 0; j < indexRecord.length; j++) {
                expandNode.splice(indexRecord[j], 1)
              }
            }
            var expandNode_after = []
            for(let i=0;i<expandNode.length;i+=1) {
              expandNode_after.push(expandNode[i].uid)
            }
            var result = expandNode_before.concat(expandNode_after).filter(function (v) {
                  return expandNode_before.indexOf(v)===-1 || expandNode_after.indexOf(v)===-1
              })
            // console.log(result)
            for(var i=0;i<result.length;i+=1){
              d3.select(".clusters").select(`#${idTransformerFrontend(result[i])}`).remove()
            }
            nodeInfo.splice(0, nodeInfo.length)
            var core_x = self.graphRender.node(v).x
            var core_y = self.graphRender.node(v).y
            
            self.lastClicked = {"id":v,"core_x":core_x,"core_y":core_y}
            // console.log(expandNode)
            frameWork(data)

            // 获取当前点击节点信息, 如果节点是最外层节点, 在 data 中查找, 否则在扩展节点中的 sub_net 中查找
            let currentNode = data.find(item => item.uid === v)

            if (!currentNode && expandNode && expandNode.length) {
              // eslint-disable-next-line no-labels
              loopExpandNode:
              for (const expand of expandNode) {
                for (const sub of expand.sub_net) {
                  if (sub.uid === v) {
                    currentNode = sub
                    // eslint-disable-next-line no-labels
                    break loopExpandNode
                  }
                }
              }
            }
            
            PosAdaption(currentNode);
          })

          self.doubleNode()
        }
        },
        // 绘制双层节点
        doubleNode:function(){

          const kernelData = this.kernelData
          const labelTransformer = this.labelTransformer
          const graph = this.graphRender
          d3.selectAll(`#svg-canvas .nodes .node`).attr("textContent",function(uid){

            
            let uid_ = labelTransformer(uid)
            const node = graph.node(uid)
            const nodeInfo = kernelData[uid_]
            const width = node.width + 20
            const height = node.height + 30
            var fill = "#fff"
            var op =node.op == "" ? "scope":node.op
            op = node.sub_net.length > 0?"scope":node.op
            if (op == "_convolution") {
              fill = "aquamarine"
            } else if (op == "batch_norm") {
              fill = "orange"
            } else if (op == "relu_" || op == "sigmoid_" || op == "tanh_") {
              fill = "chartreuse"
            } else if (op == "dropout") {
              fill = "deepskyblue"
            } else {
              fill = "wheat"
            }
            d3.select(this).selectAll("rect").attr("fill","white")

            d3.select(this).selectAll('.special-layer-2').remove()
            d3.select(this).selectAll('.special-layer-1').remove()
            d3.select(this).selectAll('.special-layer-text').remove()
            d3.select(this).selectAll('.special-layer-text2').remove()
            d3.select(this).selectAll('.header').remove()
            d3.select(this).select(".label").style("font-size","13.5px")
            let headerContainer = d3.select(this).insert("g",".label").attr("class","header").style("transform","translate(-55px,-31px)")
            headerContainer.append("rect").attr("width","110px").attr("height","1.5rem").attr("rx",10).attr("ry",10).style("fill","white").style("stroke-width","1px").style("stroke","#696969")
            headerContainer.append("circle").attr("r","8px").style("transform","translate(0.7rem,0.7rem)").style("fill",fill)
            // const kernel =node.kernel == undefined ? "none":node.kernel
            const kernel = uid_ in kernelData?kernelData[uid_].shape:"none"
            let htmlContent = undefined
            if(op =="scope"){
              let layers =  node.sub_net.length
              htmlContent=`layers:${layers}`
            } else if(op == "dropout") {
              htmlContent=`ratio:${kernel}`
            } else if(op == "batch_norm" || op == "_convolution") {
              htmlContent=`kernel:${kernel}`.replace(/ /g,"")
            }
            d3.select(this).select('.label').attr('transform', `translate(8,-${  height / 4  -2})`)
              d3.select(this).selectAll('.special-layer-2').data([0])
                .enter()
                .append('rect')
                .attr('class', 'special-layer-2')
                .style('fill', "white")
              d3.select(this).selectAll('.special-layer-2')
                .attr('x', parseFloat(-width / 2 + lineWidth))
                .attr('y', -titleHeight + titleHeight / 2 - lineWidth + 20)
                .attr('rx', cornerR + 6)
                .attr('ry', cornerR + 6)
                .attr('width', parseFloat(width - lineWidth * 2))
                .attr('height', height - titleHeight - 5)
                .style('fill', "white")
                .style('opacity', 1)
                .style('stroke-width', 0)
              d3.select(this).selectAll('.special-layer-1').data([0])
                .enter()
                .append('rect')
                .attr('class', 'special-layer-1')
                .style('fill', "white")
              d3.select(this).selectAll('.special-layer-1')
                .attr('x', -width / 2 + lineWidth)
                .attr('y', -5)
                .attr('width', width - lineWidth * 2)
                .attr('height', 15)
                .style('opacity', 1)
                .style('fill', "white")
                .style('stroke-width', 0)
              d3.select(this).selectAll('.special-layer-text1').data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 8);
              d3.select(this).selectAll('.special-layer-text').html(`op:${op}`).attr('font-size', '12px').style("transform","translate(-10px,0)");
              d3.select(this).selectAll('.special-layer-text2').data([0])
                  .enter()
                  .append('text')
                  .attr('class', 'special-layer-text')
                  .attr('x', -width / 2 + 15)
                  .attr('y', 25)
                  // .html(`kernel:${kernel}`.replace(/ /g,""))
                  .html(htmlContent)
                  .attr('font-size', '12px').style("tramsform","translate(-30px,0)").style("transform","translate(-10px,0)");;
              if(op == "linear") {
                d3.select(this).selectAll("rect").attr("fill","white")
              }
          })
        },
        // 通过节点前缀是否在展开节点列表内判断节点是否可用
        available:function(id) {
          const names = id.split('/')
          const namesLength = names.length
          if (namesLength === 1) {
            for (let i = 0; i < expandNode.length; i++) {
              if (id === expandNode[i].uid) {
                return false
              }
            }
            return true
          } else {
            let sign = 0
            const pre = names.slice(0, namesLength - 1).join('/')
            for (let i = 0; i < expandNode.length; i++) {
              if (pre === expandNode[i].uid) {
                sign = 1
                break
              }
            }
            for (let i = 0; i < expandNode.length; i++) {
              if (id === expandNode[i].uid) {
                sign = 0
                break
              }
            }
            if (sign) {
              return true
            } else {
              return false
            }
          }
        },
        // 保存节点
        nodeHold:function(nodeUid, edgeUid, srcNode, sign, op, attrs) {
          let index = -1
          for (let i = 0; i < nodeInfo.length; i++) {
            if (nodeInfo[i].uid === nodeUid) {
              index = i
              if (sign) {
                if (srcNode) {
                  nodeInfo[i].outNode.push(srcNode)
                }
                if (attrs && (JSON.stringify(attrs) !== '{}')) {
                  nodeInfo[i].attr = attrs
                }
                nodeInfo[i].op = op
              } else {
                if (srcNode) {
                  nodeInfo[i].inNode.push(srcNode)
                }
                if (attrs && (JSON.stringify(attrs) !== '{}')) {
                  nodeInfo[i].attr = attrs
                }
              }
              return true
            }
          }

          const node = { 'uid': nodeUid, 'inNode': [], 'outNode': [], 'op': '' }
          if (sign) {
            if (srcNode) {
              node.outNode.push(srcNode)
            }
            node.op = op

            if (attrs && (JSON.stringify(attrs) !== '{}')) {
              node.attr = attrs
            }
            nodeInfo.push(node)
          } else {
            if (srcNode) {
              node.inNode.push(srcNode)
            }
            if (attrs && (JSON.stringify(attrs) !== '{}')) {
              node.attr = attrs
            }
            nodeInfo.push(node)
          }
        },
        successor:function(itemnode, success) {
          const g = this.graphRender
          const successors = g.successors(itemnode)
          if (successors.length != 1 || g.predecessors(successors[0]).length > 1) {
            success["tag"] = false
            return
          }
          if (g.node(successors[0]).op == "_convolution") {
            var id = successors[0]
            var idt = this.idTransformer(successors[0])
            success["conv2"] = {"r":id,"t":idt}
            success["tag"] = true
            return
          }
          if (g.node(successors[0]).op == "linear") {
            var id = successors[0]
            var idt = this.idTransformer(successors[0])
            success["linear"] = {"r":id,"t":idt}
            success["tag"] = true
            return
          }
          if (g.node(successors[0]).op == "batch_norm") {
            var id = successors[0]
            var idt = this.idTransformer(successors[0])
            success["bn"] = {"r":id,"t":idt}
            this.successor(successors[0],success)
            return
          }
          if (g.node(successors[0]).op == "relu_" || g.node(successors[0]).op == "relu") {
            var id = successors[0]
            var idt = this.idTransformer(successors[0])
            success["relu"] = {"r":id,"t":idt}
            this.successor(successors[0],success)
            return 
          }
          if (g.node(successors[0]).op.search(/pool/i) >= 0) {
            this.successor(successors[0],success)
          }else if(g.node(successors[0]).op.search(/dropout/i) >= 0){
            this.successor(successors[0],success)
          }else if(g.node(successors[0]).op.search(/view/i) >= 0){
            this.successor(successors[0],success)
          } else {
            success["tag"] = false
            return 
          }
        },
        del:function(id,i) {
          this.saved.splice(i,1)
        },
        // 处理节点信息，存入saved
        addSave:function(node) {
          var tmp = {}
          var id = node.id
          var id_ = id.split("/")
          tmp["id"] = id_[id_.length - 1]
          tmp["kernel"] = node.kernel
          tmp["op"] = node.op
          tmp["uid"] = node.id
          var options = this.options
          var search = function(options_,idIndex){
            // 查找完成，返回
            if(idIndex>id_.length){
              return
            }
            var prefix = id_.slice(0,idIndex).join("/")
            // 在当前找到前缀，则从前缀子目录下继续查找
            for(var i=0; i<options_.length; i+=1) {
              if(options_[i].value == prefix) {
                search(options_[i].children,idIndex+1)
                return
              }
            }
            // 当前无此前缀，迭代生成
            for(var i = idIndex;i<=id_.length;i+=1) {
              var obj = {}
              obj["uid"] = node.id
              obj["kernel"] = node.kernel
              obj["op"] = node.op
              obj["label"] = id_[idIndex-1]
              obj["value"] = id_.slice(0,idIndex).join("/")
              if(i<id_.length) {
                obj["children"] = []
                options_.push(obj)
                options_ = obj["children"]
                idIndex += 1
              } else {
                options_.push(obj)
              }
            }
            return
          }
          search(options,1)
          if(this.saved.indexOf(node)<0) {
            this.saved.push(node)
          }
        },
        // 节点导航
        nagigation:function(node) {
          // console.log(node)
          var data= this.structData
          // var uid = node.uid
          var uid = node
          var uid_ = uid.split("/")
          var length = uid_.length
          var tag = 0 // tag标记有没有在展开节点列表内找到前缀
          var idTransformerFrontend = this.idTransformerFrontend
          // 扩展节点中没找到时，从源数据中查找
          function update(index) {
            if(index == length) {
              return
            }
            var id = uid_.slice(0,index).join("/")
            for(var i=0;i<data.length;i+=1) {
              if(data[i].uid == id) {
                expandNode.push({
                  'uid': id,
                  'layer': data[i].layer,
                  'sub_net': data[i].sub_net,
                  'label': data[i].label,
                })
                data = data[i].sub_net
                break
              }
            }
            update(index+1)
          }
          var ind = 1
          for(;ind<uid_.length;ind+= 1){
            for (var i=0;i<expandNode.length;i+=1){
              //  展开节点列表内找到前缀,data更新，tag记1
              var id = uid_.slice(0,ind).join("/")
              if(expandNode[i].uid == id) {
                data = expandNode[i].sub_net
                tag = 1
              }
            }
            //  如果没找到，从源数据中找
            if(tag == 0) {
              update(ind)
              break
            }
            tag = 0
          }
          // dagre绘制时直接改变源数据
          var data = this.structData
          this.frameWork()

          let currentNode = data.find(item => item.uid === uid)

          if (!currentNode && expandNode && expandNode.length) {
            // eslint-disable-next-line no-labels
            loopExpandNode:
            for (const expand of expandNode) {
              for (const sub of expand.sub_net) {
                if (sub.uid === uid) {
                  currentNode = sub
                  // eslint-disable-next-line no-labels
                  break loopExpandNode
                }
              }
            }
          }
          this.PosAdaption(currentNode);
        },
        // 测试function
        test:function(val) {
          this.nagigation(val[val.length -1])
        },
        delOption(data) {
          var path=data.pathLabels
          var options_ = this.options
          var search = function(options,index) {
            for(var i=0;i<options.length;i+=1){
              if(options[i].label == path[index]) {
                console.log(options[i].label)
                if(options[i].children == undefined) {
                  options.splice(i,1)
                  return
                } else {
                  search(options[i].children,index+1)
                  if(options[i].children.length == 0) {
                    options.splice(i,1)
                    return
                  }
                }
              }
            }
          }
          let dropNode = this.idTransformer(data.value)
          this.monitor({"monitorList":dropNode,"tag":"drop"})
          search(options_,0)
        },
        drawHistory() {
          let self = this
          d3.select('#history').selectAll(".node").remove()
          d3.select('#history').selectAll(".edge").remove()
          for(let i=0;i<this.historyData_.length;i+=1){
            for(let j=0;j<this.historyData_[i].length;j+=1){
              if(this.historyData_[i][j] != undefined){
                this.historyNode(this.historyData_[i][j],j,i)
              }
            }
          }
          var {width,height} = d3.select("#history").select("#nodes").node().getBBox()
          d3.select('#history').style("height",height+40).style("width",width+40)
          this.historyMenuNode("Saved")
          d3.select("#history").select("#nodes").selectAll(".virNode").style("stroke-opacity",0)
          d3.select(self.idTransformerFrontend(`#${self.nowStatus.id}`)).select(".virNode").style("stroke-opacity",1)
        },
        historyMenu(content){
          let self = this
          self.virNodeId = 0
          // let uid = `t${self.nowStatus.ancestor}/${self.modelAmount.toString()}-${self.virNodeId}-${"TRUE"}`
          let uid = `t${self.nowStatus.ancestor}/${self.modelAmount.toString()}-${self.virNodeId}-${"Saved"}`
          let ancestor = self.nowStatus.ancestor
          // if(self.nowStatus.tag == "Saved") {
            ancestor = `${ancestor}/${self.modelAmount}`
          // }
          // let newStatus = {"uid":uid,"name":self.modelAmount.toString(),"tag":"TRUE","ancestor":`${ancestor}`,"children":[],"label":self.modelAmount.toString()}
          let x = self.historyData_[self.nowStatus.pos[1]+1]?self.historyData_[self.nowStatus.pos[1]+1].length:0
          let newStatus = {"id":uid,"name":self.modelAmount.toString(),"type":"Saved","ancestor":`${ancestor}`,"label":`v${self.virNodeId.toString()}`,"pPos":self.nowStatus.pos,"pos":[x,self.nowStatus.pos[1]+1],"acc":parseFloat(self.get_scalar_data["acc"][self.get_scalar_data["acc"].length-1]).toFixed(0)/100,"loss":parseFloat(self.get_scalar_data["loss"][self.get_scalar_data["loss"].length-1]).toFixed(2)/100,"parent":self.nowStatus.id,"children":[],"content":content,"lr":self.lr,"batch":self.batch,"step":self.get_scalar_data["step"][self.get_scalar_data["step"].length-1]}
          
          self.modelAmount += 1
          
          

          if(self.historyData_.length>self.nowStatus.pos[1]+1){
            // self.historyData_[self.nowStatus.pos[1]+1].push(newStatus)
            let index = self.nowStatus.pos[0]
            while(true){
              if(self.historyData_[self.nowStatus.pos[1]+1][index] == undefined){
                newStatus[0] = index
                self.historyData_[self.nowStatus.pos[1]+1][index] = newStatus
                break
              } else {
                index += 1
              }
            }
          } else {
            // self.historyData_.push([newStatus])
            self.historyData_.push([])
            newStatus.pos[0] = self.nowStatus.pos[0]
            self.historyData_[self.historyData_.length-1][self.nowStatus.pos[0]] = newStatus
          }
          console.log(self.nowStatus.pos,newStatus.pos)
          self.nowStatus.children.push(newStatus)
          self.nowStatus = newStatus
          
          self.drawHistory()
          if(content == "Saved"){
            self.setKeepTag({"keep":"1","dataRoute":"","structureRoute":""})
          } else {
            this.$nextTick(()=>window.setTimeout(()=>{this.featchKernel({"prun":true})},3000))
          }
          // console.log(this.nowStatus)
          
        },
        historyMenuNode(){
          let {idTransformerFrontend,gh,bank,activate} = this
          let self = this

          function DFS(node,uid,ancestor){
            if(ancestor.indexOf(node.ancestor) == 0) {
              if(uid == node.uid) {
                self.nowStatus = node
              }
            }
          }

          d3.select("#history").select("#nodes").on("click",function(){
              let bubblePath = d3.event.path
              for(let i of bubblePath){
                if(i.id){
                  
                  let [x,y] = d3.select(self.idTransformerFrontend(`#${i.id}`)).attr("pos").split(",").map((n)=>{return parseInt(n)})
                  let type = d3.select(self.idTransformerFrontend(`#${i.id}`)).attr("type")
                  let ancestor = d3.select(self.idTransformerFrontend(`#${i.id}`)).attr("ancestor")
                  if(type === "NotSaved"){
                    if(ancestor != self.nowStatus.ancestor) {
                      return
                    } else {
                      self.nowStatus = self.historyData_[y][x]
                      self.nowStatus.children.splice(0,1)
                      self.virNodeId = parseInt(self.nowStatus.label.slice(1)) + 1

                      if(y>=self.historyData_.length-1){
                      } else {
                        let pos = [x,y]
                        for(let j=y+1;j<self.historyData_.length;j+=1){
                          for(let k=0;k<self.historyData_[j].length;k+=1){
                            if(self.historyData_[j][k] == undefined){
                              continue
                            }
                            if(self.historyData_[j][k].pPos[1] === pos[1] && self.historyData_[j][k].pPos[0] === pos[0]){
                              self.historyData_[j][k] = undefined
                              pos = [k,j]
                              break
                            }
                          }
                        }
                      }

                      // self.drawHistory()
                      let dataRoute = `${self.nowStatus.ancestor}/${parseInt(self.nowStatus.name.slice(1))}`
                      self.setKeepTag({"keep":"3","dataRoute":dataRoute,"structureRoute":""})
                      let timer = setTimeout(function(){self.featchKernel({});clearTimeout(timer)},1000)
                    }
                  } else {
                    self.nowStatus = self.historyData_[y][x]
                    self.virNodeId = 0
                    self.modelAmount += 1
                    // self.drawHistory()
                    
                    self.setKeepTag({"keep":"2","dataRoute":"","structureRoute":`${self.nowStatus.ancestor}`})
                    let timer = setTimeout(function(){self.featchKernel({});clearTimeout(timer);self.setLr({"lr":self.lr});self.setBatchsize({"batchsize":self.batch})},1000)
                    self.lr = self.nowStatus.lr
                    self.batch = self.nowStatus.batch
                    
                  }
                  d3.select("#history").select("#nodes").selectAll(".virNode").style("stroke-opacity",0)
                  d3.select(self.idTransformerFrontend(`#${i.id}`)).select(".virNode").style("stroke-opacity",1)
                  
                  break
                }
              }
          })

          $('#history').contextMenu({
            selector: '.node',
            items: {
              save: {
                name: 'compare',
                icon: 'load',
                callback() {
                  let id = this[0]["id"]
                  // let target = d3.select(d3.select(`#${idTransformerFrontend(id)}`).selectAll("rect")['_groups'][0][1])
                  let target = d3.select(`#${idTransformerFrontend(id)}`).select("circle")
                  let dPath = d3.select(this[0]).attr("ancestor")
                  if(dPath in self.getCompare){
                    // let color = target.style("stroke")
                    let color = target.style("fill")
                    let pos = activate.indexOf(color)
                    let newObj = {}
                    activate.splice(pos,1)
                    // target.style("stroke","rgb(103, 194, 58)")
                    target.style("fill","white")
                    target.style("visibility","hidden")
                    delete self.getCompare[dPath]
                    for(let i in self.getCompare){
                      newObj[i] = self.getCompare[i]
                    }
                    self.setCompare(newObj)
                    
                  } else {
                    if(activate.length>4){
                      return
                    }
                    let difference = [...new Set(bank.filter(x=>!activate.includes(x)))]
                    // target.style("stroke",difference[0])
                    target.style("fill",difference[0])
                    target.style("visibility","visible")
                    activate.push(difference[0])
                    self.fetchTrainData({"dPath":dPath,"color":difference[0]})
                  }
                }
              },
            
            }
          })


        },
        historyNode(data, i,j){
          let strokeColor = {"Saved":"#67C23A","NotSaved":"#EB6100"}
          let fill = {"Saved":"savedLinear","NotSaved":"notSavedLinear"}
          let color = strokeColor[data["type"]]
          // console.log(data["type"])
          let node = d3.select("#history #nodes").append("g").attr("id",data.id).attr("class","node").attr("ancestor",data.ancestor)
          node.attr("pos",[i,j]).attr("type",data["type"]).attr("ancestor",data["ancestor"])
          let width = 130
          let height = width/2
          let scale = 0.7
          // this.rContorl()
          // node.append("rect").attr("x",i*(width+20)+10-3).attr("y",j*width*scale+10-3).attr("width",width+6).attr("height",height+6).style("fill","white").attr("rx","20px").attr("rx","20px")
          //   .style("stroke","#707070").style("stroke-width","3px").style("stroke-dasharray",5).style("fill-opacity",0).style("stroke-opacity",0).attr("class","virNode")
          node.append("rect").attr("x",i*(width+20)+10-3).attr("y",j*width*scale+10-3).attr("width",width+6).attr("height",height+6).style("fill","white").attr("rx","20px").attr("ry","20px")
            .style("stroke","#67C23A").style("stroke-width","5px").style("fill-opacity",0).style("stroke-opacity",0).attr("class","virNode").attr("filter","url(#blur-2px)")
          node.append("rect").attr("x",i*(width+20)+10-0.1*width).attr("y",j*width*scale+10-0.25*height).attr("width",width*1.3).attr("height",height*1.5).style("fill","transparent").attr("rx","20px").attr("rx","20px").style("stroke","white").style("stroke-width","5px")
          node.append("rect").attr("x",i*(width+20)+10).attr("y",j*width*scale+10).attr("width",width).attr("height",height).style("fill",`url(#${fill[data["type"]]})`).attr("rx","20px").attr("rx","20px")
            .style("stroke",color).style("stroke-width","3px")
            // .attr("filter","url(#blur-2px)")
          // data.content ="dsfdojrgoregnrenogpsim"
          let content1 = data.content
          let content2 = ""

          if(content1.length>20){
            content1 = data.content.slice(0,20)
            content2 = data.content.slice(20)
          }
          // console.log(content)
          node.append("text").attr("x",i*(width+20)+10+width/2).attr("y",j*width*scale+10+11).attr("text-anchor","middle").html(content1).style("font-size","10px")
          node.append("text").attr("x",i*(width+20)+10+width/2).attr("y",j*width*scale+10+11+13).attr("text-anchor","middle").html(content2).style("font-size","10px")
          node.append("circle").attr("cx",i*(width+20)+10+width).attr("cy",j*width*scale+10).attr("r",5).style("fill","white").style("visibility","hidden")
          if(!data.lr){
            data.lr = this.getLr
            data.batch = this.getBatch
            data.step = 0
          }
          
          let toolTip = node.append("g").style("transform","translate(0,3px)")
          toolTip.append("text").attr("x",i*(width+20)+10+6).attr("y",j*width*scale+10+height-height/3*1.5).html(`lr:${data.lr}`).style("font-size","12px")
          toolTip.append("text").attr("x",i*(width+20)+10+6).attr("y",j*width*scale+10+height-height/3*1).html(`batch:${data.batch}`).style("font-size","12px")
          toolTip.append("text").attr("x",i*(width+20)+10+6).attr("y",j*width*scale+10+height-height/3*0.5).html(`step:${data.step}`).style("font-size","12px")
          toolTip.append("rect").attr("x",i*(width+20)+10+6+(width/2)).attr("y",j*width*scale+10+height-height/3*2+3).attr("width",width/2-12).attr("height",height/3-5).attr("rx","10px").attr("rx","10px")
            .style("fill","#EEEEEE")
          toolTip.append("rect").attr("x",i*(width+20)+10+6+(width/2)).attr("y",j*width*scale+10+height-height/3*2+3).attr("width",(width/2-12)*data.acc).attr("height",height/3-5).attr("rx","10px").attr("rx","10px")
            .style("fill","#00A0E9")
          toolTip.append("text").attr("x",i*(width+20)+10+6+(width/2)).attr("y",j*width*scale+10+height-height/3*2 + (height/3-2)).attr("dy","-0.2em").attr("dx","0.2em").html(`${(data.acc*100).toFixed(0)}%`).style("font-size","12px")
          // toolTip.append("rect").attr("x",i*(width+20)+10+6+(width/2)).attr("y",j*width*scale+10+height-height/3).attr("width",width/2-12).attr("height",height/3-5).attr("rx","10px").attr("rx","10px")
          //   .style("fill","#EEEEEE")
          
          // toolTip.append("rect").attr("x",i*(width+20)+10+6+(width/2)).attr("y",j*width*scale+10+height-height/3-4).attr("width",(width/2-12)*data.loss).attr("height",height/3-2).attr("rx","10px").attr("rx","10px")
          //   .style("fill","rgb(25, 114, 187)")
          // 
          toolTip.append("text").attr("x",i*(width+20)+10+6+(width/2)).attr("y",j*width*scale+10+height-height/3*0.5).attr("dx","0.2em").html(`loss:${(data.loss*100).toFixed(2)}`).style("font-size","12px")
          if(data.parent){
            this.historyEdge({"id":data.id,"pos":[i,j]},{"id":data.parent,"pos":data.pPos})
          }
        },
        historyEdge(to,from){
          // console.log(from,to)
          let edge = d3.select("#history #edges").append("g").attr("id",`${from.id}-${to.id}`).attr("class","edge")
          let width = 130
          let height = width/2
          let scale = 0.7
          const lineFunction = d3
              .line()
              .x(function(d,i) {
                return d[0]*(width+20)+10-3+width/2
              })
              .y(function(d,i) {
                
                if(i===3){
                  return d[1]*width*scale+10-3
                } else if(i===1){
                  return d[1]*width*scale+10-3-(width*scale-height)/2
                } else if(i===0){
                  return d[1]*width*scale+10-3+height
                }else{
                  return d[1]*width*scale+10-3-(width*scale-height)/2
                }
              })
          let pathData = []
          pathData.push(from.pos)
          pathData.push([from.pos[0],to.pos[1]])
          pathData.push([to.pos[0],to.pos[1]])
          pathData.push(to.pos)

          // console.log(pathData)

          edge.selectAll('path')
          .data([pathData])
          .enter()
          .append('path')
          .attr('fill', 'none')
          .attr('stroke',"#67C23A")
          .attr('d', function(d) {
            return lineFunction(d)
          })
          // .attr("marker-start","url(#dot)")
          .attr("marker-end","url(#markerArrow)")
        },
        
        
    },
}
</script>

<style lang="less" scoped>
@import 'Layout.less';
</style>

