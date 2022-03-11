/*
 * @Author: your name
 * @Date: 2021-03-24 10:56:24
 * @LastEditTime: 2021-11-21 16:34:00
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \prunfrontend\src\store\modules\layout.js
 */
import http from '@/utils/request'
import port from '@/utils/api'
import qs from 'qs'
const state = {
    image:[],
    predict:[]
}

const getters = {
    getImage:(state)=>state.image,
    getPredict:(state)=>state.predict
}

const actions = {
    async fetchTestData(context, params) {
        await http.useGet(port.category.test, params)
            .then(res => {
                context.commit('setTestData', res.data.data)
        })
    },
}

const mutations = {
    setTestData(state,param){
        state.image = param.data
        state.predict = param.res
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }