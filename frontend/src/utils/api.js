/*
 * @Author: your name
 * @Date: 2021-03-24 10:26:22
 * @LastEditTime: 2022-01-10 16:53:23
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \prunfrontend\src\components\utils\api.js
 */
export default {
    manage: {
      waitingPage: '/api/init'
    },
    category: {
      test:'/api/testData',
      structure: '/api/structure',
      rank:'/api/rank',
      parameters:'/api/parameters',
      sensitivity:'/api/sensitivity',
      scalar:'/api/scalar',
      weight:'/api/weight',
      weightGrad:'/api/weightGrad',
      bias:'/api/bias',
      biasGrad:'/api/biasGrad',
      rControl:'/api/rControl',
      cControl:'/api/cControl',
      prun:'/api/prun',
      monitor:'/api/monitor',
      cycle:'/api/cycle',
      node:'/api/tempData',
      palyTag:'/api/palyTag',
      batchsize:'/api/batchsize',
      dropout:'/api/dropout',
      trainCycle:'/api/trainCycle',
      lr:'/api/lr',
      keep:'/api/keep',
      train:'/api/trainData',
      model:'/api/modelTxt',
      automlList:'/api/automlList',
      automlGraph:'/api/automlGraph',
      automlProcess:'/api/automlProcess',
      automlRough:'/api/rough',
      graph:'/api/graph'
    }
  }