
/*
 * @Author: your name
 * @Date: 2021-03-24 10:56:24
 * @LastEditTime: 2022-01-27 17:52:55
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \prunfrontend\src\store\modules\layout.js
 */
import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
const state = {
  automlList:[],
  modelGraph:null,
  sortKey:0
}

const getters = {
  getAutomlList:(state) => {
    state.automlList.sort(function(a, b){return parseFloat(b[state.sortKey])-parseFloat(a[state.sortKey])})
    return state.automlList
  },
  getAutomlGraph:(state) => state.modelGraph
}

const actions = {
  // 性能数据
  async fetchAutomlData(context, params) {
    await http.useGet(port.category.automlList, params)
        .then(res => {
            context.commit('setAutoml', res.data.data)
    })
  },
  // 具体模型结构数据
  async fetchAutomlModelGraph(context, params) {
    await http.useGet(port.category.automlGraph, params)
        .then(res => {
            context.commit('setAutomlGraph', res.data.data)
    })
  },
  // automl执行
  async automlProcess(context, params) {
    await http.useGet(port.category.automlProcess, params)
        .then(res => {
    })
  },
}

const mutations = {
  setAutoml(state,param){
    state.automlList = param
  },
  setAutomlGraph(state,param){
    state.modelGraph = param
  },
  setSortKey(state,param){
    state.sortKey = param
  }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }