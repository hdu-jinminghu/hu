<template>
<div :class="['selector-group']">
  <el-select v-model="optim" placeholder="optims">
    <el-option
      v-for="item in optims"
      :key="item"
      :label="item"
      :value="item">
    </el-option>
  </el-select>
  <el-select v-model="dataset" placeholder="dataset">
    <el-option
      v-for="item in datasets"
      :key="item"
      :label="item"
      :value="item">
    </el-option>
  </el-select>
  <el-select v-model="loss" placeholder="loss">
    <el-option
      v-for="item in lossFcs"
      :key="item"
      :label="item"
      :value="item">
    </el-option>
  </el-select>
</div>
</template>

<script>
import 'element-ui/lib/theme-chalk/index.css'
import method from './hyper.method'
import {optims,lossFcs, datasets} from '../init'
export default {
    data() {
        return {
            lossFcs: [],
            datasets: [],
            optims:[],
            loss: 'CrossEntropyLoss',
            dataset:'CIFAR10',
            optim:'SGD'
        }
    },
    mounted(){
        this.lossFcs = lossFcs
        this.datasets = datasets
        this.optims = optims
    },
    methods:{
        ...method,
    }
}
</script>

<style lang="less" scoped>
@import 'hyper.less';
</style>

