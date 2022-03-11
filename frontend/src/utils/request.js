/*
 * @Author: your name
 * @Date: 2021-03-24 10:19:47
 * @LastEditTime: 2021-12-29 21:45:14
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \prunfrontend\src\components\utils\request.js
 */
import axios from 'axios'
import constants from './constants'
import store from '../store/modules/modelView'  
import store_ from '../store/modules/editor'  

const service = axios.create({
  baseURL: constants.DJANGOHOSTNAME,
  timeout: 350000,  
})
// service.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
// 请求拦截,暂时未用
service.interceptors.request.use(
  function(config) {
    return config
  },
  error => {
    console.log('error', error)
    return Promise.reject(error)
  }
)

// 响应拦截,暂时未用
service.interceptors.response.use(
  function (response) {
    return response
  },
  function(error) {
    return Promise.reject(error)
  }
)

const useGet = (url, params) => {
  const user = store.state
  // const user = "test"
  params['job'] = user.modelName || ""
  // params['job'] = "test"
  params['dataset'] = user.dataset
  if(Object.keys(params).indexOf("g")>=0){
    if(user.state == "generator"){
      params["g"] = ""
      user.state = "reload"
    }
  }
  return service.get(url, { params })
}

const usePost = (url, jsonData) => {
  const user = store.state
  jsonData['job'] = user.modelName
  if(Object.keys(jsonData).indexOf("g")>=0){
    if(jsonData["g"] == "generator"){
      user.state = "generator"
    } else {
      if(user.state == "generator"){
        jsonData["g"] = ""
        // jsonData["g"] == "generator"
        user.state = "reload"
      }
    }
  }
  jsonData["g"] == "generator"
  return service.post(url, jsonData)
}

export default { useGet, usePost }