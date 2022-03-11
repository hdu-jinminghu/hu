
import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
const state = {
  dir:'',
  lr:0.01,
  batch:100,
  compareColor:{"red":false,"green":false,"blue":false,"#7fccff":false,"#caff7f":false}
}

const getters = {
  getLr:(state)=>state.lr,
  getBatch:(state)=>state.batch,
  getConfig:(state)=>{
    return {'lr':state.lr,'batch':state.batch}
  },
  getDebugDir:(state)=>state.dir,
  getCompareColor:(state)=>state.compareColor
}

const actions = {
  async setKeepTag(context,params){
    await http.useGet(port.category.keep, params)
  },
  async setPlayTag(context,params) {
    await http.useGet(port.category.palyTag, params)
  },
  async setLr(context,params) {
    state.lr = params["lr"]
    await http.useGet(port.category.lr, params)
  },
  async setBatchsize(context,params) {
    state.batch = params["batchsize"]
    await http.useGet(port.category.batchsize, params)
  },
}

const mutations = {
  setDebugDir:function(state,dir){
    state.dir = dir
  },
  setLr:function(state,lr){
    state.lr = lr
  },
  setBatch:function(state,batch){
    state.batch = batch
  }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }