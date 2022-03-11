import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
const state = {
  finish_state:{"rank":false,"sensitivity":false},
  indicator:{"rank":[],"sensitivity":[]},
  prun_tag:true,
  target:{"conv1":undefined,"bn2d":undefined,"conv2":undefined}, // 参数修剪目标 
  targetVertex:{"conv1":undefined,"bn2d":undefined,"conv2":undefined}, // 数据节点
}

const getters = {
  get_finish_state:(state)=>state.finish_state,
  get_indicator:(state)=>state.indicator,
  get_prun_tag:(state)=>state.prun_tag,
  get_targetVertex:(state)=>state.targetVertex,
}

const actions = {
  async fetch_rank(context, params) {
    await http.useGet(port.category.rank, params)
        .then(res => {
            context.commit("set_rank",res.data.data["rank"])
    })
  },
  async fetch_sensitivity(context,params) {
    await http.useGet(port.category.sensitivity, params)
        .then(res => {
            context.commit("set_sensitivity",res.data.data["sensitivity"])
    })
  },
  async directive_prun(context,params) {
    params = {...params,...state.target}
    state.target.conv2 &&
    await http.usePost(port.category.prun, params)
  },
}

const mutations = {
  set_rank(state, param) {
    state.rank = param
    let finish_state = {}
    finish_state["rank"] = true
    finish_state["sensitivity"] = state.finish_state["sensitivity"]
    state.finish_state = finish_state
    
  },
  set_sensitivity(state, param) {
    state.sensitivity = param
    let finish_state = {}
    finish_state["rank"] = state.finish_state["rank"]
    finish_state["sensitivity"] = true
    state.finish_state = finish_state
  },
  set_indicator(state) {
    state.indicator = {"rank":state.rank,"sensitivity":state.sensitivity}
  },
  reset_finish_state(state) {
    let finish_state = {}
    finish_state["sensitivity"] = false
    finish_state["rank"] = false
    state.finish_state = finish_state
  },
  set_prun_target(state,params) {
    state.target = params
  },
  set_prun_targetVertex(state,params){
    state.targetVertex = params
  },
  set_prun_tag(state) {
    state.prun_tag = !state.prun_tag
  },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }