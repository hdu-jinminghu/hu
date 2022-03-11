import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
const state = {
  scalar_data:{"acc":[],"loss":[],"step":[],"breakpoints":[]},
}

const getters = {
  get_now_status:(state)=>{
    let epochs = state.scalar_data["loss"].length
    let loss = state.scalar_data["loss"][epochs-1]
    loss = parseFloat(loss).toFixed(2)
    let acc = state.scalar_data["acc"][epochs-1]
    acc = parseFloat(acc).toFixed(2)
    let step = state.scalar_data["step"][epochs-1]
    return {"loss":loss,"acc":acc,"step":step}
  },
  get_scalar_data:(state)=>state.scalar_data,
}

const actions = {
  async fetch_scalar(context,params) {
    await http.useGet(port.category.scalar, params)
        .then(res => {
            context.commit("set_scalar_data",res.data.data)
    })
  },
}

const mutations = {
  set_scalar_data(state, data) {
    if (state.scalar_data["acc"].length != data["tol"][0].length){
      let new_scalar_data = {}
      new_scalar_data["breakpoints"] = data["breakpoints"]
      new_scalar_data["acc"] = data["tol"][0]
      new_scalar_data["loss"] = data["tol"][1]
      new_scalar_data["step"] = data["tol"][2]
      state.scalar_data = new_scalar_data
    }
  },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }