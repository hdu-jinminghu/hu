
import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
import { satisfies } from 'semver'
const state = {
    dataset:"CIFAR10",
    modelName:'',
    graph:{"nodeList":[],"lineList":[]}
}

const getters = {
    getDataset:(state)=>state.dataset,
    getModelName:(state)=>state.modelName,
    getGraph:(state)=>state.graph
}

const actions = {
}

const mutations = {
    set_dataset(state,param){
        state.dataset = param
    },
    set_modelname(state,param){
        state.modelName = param
    },
    set_graph(state,param){
        state.graph = param
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }