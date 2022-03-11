
import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
const state = {
  compareData:{}
}

const getters = {
  getCompare:(state)=> state.compareData,
}

const actions = {
  async fetchTrainData(context, params) {
    await http.useGet(port.category.train, params)
        .then(res => {
            context.commit('setTrainData', res.data.data)
    })
},
}

const mutations = {
  setTrainData(state,param){
    let id = param["dPath"]
    let loss = param["loss"]
    let acc = param["acc"]
    let step = param["step"]
    let color = param["color"]
    let obj = {}
    state.compareData[id] = {"loss":loss,"acc":acc,"step":step,"color":color}
    for(let i in state.compareData){
        obj[i] = state.compareData[i]
    }
    state.compareData = obj
  },
  delTrainData(state,param){
    let obj = JSON.parse(JSON.stringify(state.compareData))
    delete obj[param]
    state.compareData = obj
  }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }