import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
import {vgg16,resnet50} from '@/components/build/template'
import { param } from 'jquery'
const state = {
  dragItem:null,
  changeItem:null,
  dir:null,
  moduleList:{},
  modelGraphList:{},  // 模型信息
  modelList:[], // 保存模型名
  modelName:'test',
  dataset:'CIFAR10',
  activeModule:'',
  stage:'graph',
  trainStep:undefined, // 剪枝数据当前迭代步
  targetVertex:undefined, // 剪枝选中节点
  moduleCe:{},
  applyModule:[],
  prunContent:'',
  graph:undefined,
  channels:{"channels":0},
  autoModuleList:[],
  tol:0,
}

const getters = {
  getGraph:(state)=>state.graph,
  getDragIem:(state)=>state.dragItem,
  getChangeItem:(state)=>state.changeItem,
  getDir:(state)=>state.dir,
  getModulId:(state)=>state.moduelId,
  getModuleList:(state)=>state.moduleList,
  getActiveModule:(state)=>state.moduleList[state.activeModule],
  getGlobalStage:(state)=>state.stage,
  getTrainStep:(state)=>state.trainStep,
  getTargetVertex:(state)=>state.targetVertex,
  getModuleCe:(state)=>state.moduleCe,
  getPrunContent:(state)=>state.prunContent,
  getChannels:(state)=>state.channels,
  getAutoModuleList:(state)=>state.autoModuleList,
  getTol:(state)=>state.tol
}

const actions = {
  async genereModel(context,params) {
    params["job"] = state.modelName
    params["lossFc"] = state.modelGraphList[params["job"]]["lossFc"]
    params["dataset"] = state.modelGraphList[params["job"]]["dataset"]
    
    context.commit("reset")
    await http.usePost(port.category.model, params)
        .then(res => {
            console.log(res)
    })
  },
  async setInitData(context,params) {
    let id = `${state.stage}/${params['Id']}`
    let id_ = id.split("/")
    id_.splice(0,1)
    
    params['Id'] = '*' + id_.join('*')
    state.targetVertex = params['Id']
    await http.useGet(port.category.node, params)
        .then(res => {
          if(res.status == 200){
            context.commit("setTrainStep", res.data.data)
          }
    })
  },
  // 模块生成
  async roughAutoml(context,params) {
    params["job"] = state.modelName
    params["lossFc"] = state.modelGraphList[params["job"]]["lossFc"]
    params["dataset"] = state.modelGraphList[params["job"]]["dataset"]
    state.tol = params["tol"]
    let moduleAbleDic = {}
    state.applyModule.forEach((v)=>{
      state.moduleCe[v].forEach((u)=>{
        v == u || (moduleAbleDic[u] = state.moduleList[u])
      })
    })
    params["moduleAble"] = moduleAbleDic
    params['automlM'] = state.autoModuleList
    await http.usePost(port.category.automlRough, params)
  },
  // 保存、取回模型结构数据
  // params{"op":"save"/"fetch","graph":}
  async dealgraph(context,params) {
    params["graph"] = state.graph
    await http.usePost(port.category.graph, params).then(res => {
      context.commit("restoreGraph",res.data.data)
    })
  },
}

const mutations = {
  setActiveModule:function(state,moduleId){
    state.activeModule = moduleId
  },
  setDragItem:function(state,item){
    state.dragItem = item
  },
  changeItemInfo:function(state,item){
    if(item["lineList"]!=undefined){
      return
    }else{
      state.changeItem = item
    }
   
  },
  setDir:function(state,dir){
    state.dir = dir
  },
  setModelSData(state,params){
    let [modelName,sData,lossFc,dataset] = params
    if(state.modelList.indexOf(modelName)<0){
        state.modelList.push(modelName)
    }
    state.modelName = modelName
    state.dataset = dataset
    state.lossFc = lossFc
    state.modelGraphList[modelName] = {"sData":JSON.parse(JSON.stringify(sData)),"lossFc":lossFc,"dataset":dataset}
  },
  reset(state){
    state.lr = 0
    state.cycle = 0
    state.batch = 0
    state.epoch = 0
    state.monitor = []
  },
  setModuleId(state,id){
    state.moduelId = id
  },
  initModule(state,moduleList){
    let ml = {}
    for(let module in moduleList){
      let obj = {}
      obj['type'] = `module_${module}`
      obj['typeName'] = module
      obj['nodeName'] = module
      obj['attrs'] = moduleList[module]['attrs']
      obj['log_bg_color'] = 'rgba(250, 205, 81, 0.2)'
      obj['lineList'] = moduleList[module]['lineList']
      obj['nodeList'] = moduleList[module]['nodeList']
      ml[module] = obj
    }
    state.moduleList = ml
  },
  setModuleData(state,param){
    param['type'] = `module_${state.moduelId}`
    param['typeName'] = state.moduelId
    param['nodeName'] = state.moduelId
    param['attrs'] = {}
    param['log_bg_color'] = 'rgba(250, 205, 81, 0.2)'
    let ml = {}
    for(let module in state.moduleList){
      ml[module] = state.moduleList[module]
    }
    ml[state.moduelId] = param
    state.moduleCe['common'].push(state.moduelId)
    state.moduleList = ml
  },
  setGlobalStage(state,stage){
    state.stage = stage
  },
  setTrainStep(state,param) {
    state.trainStep = param["step"]
  },
  setModuleCategory(state,param){
    state.moduleCe['common'] = []
    state.moduleCe['Lenet'] = param[4]
    state.moduleCe['Alexnet'] = param[3]
    state.moduleCe['vgg16'] = param[1]
    state.moduleCe['resnet50'] = param[0]
    state.moduleCe['googlenet'] = param[2]
    
  },
  setApplyModule(state,param){
    state.applyModule = param
  },
  setPrunContent(state,content){
    state.prunContent = state.stage + "/" + content
  },
  setOriGraph(state,graph){
    state.graph = graph
  },
  restoreGraph(state,graph){
    console.log(graph)
    if(graph == "success"){
      return
    } else {
      state.graph = graph
    }
  },
  setChannels(state,channels){
    state.channels = {"channels":channels}
  },
  setAutomlM(state,autoModuleList){
    
    let temp = []
    for(let autoModule of autoModuleList){
      let obj = {}
      obj["channels"] = autoModule["attrs"]["channels"]
      obj["deepth"] = autoModule["attrs"]["deepth"]
      obj["type"] = autoModule["type"]
      temp.push(obj)
    }
    state.autoModuleList = temp
  }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }