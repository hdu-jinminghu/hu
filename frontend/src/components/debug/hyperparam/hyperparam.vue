<template>
    <div :class="['debug-hyperparam']">
        <el-input placeholder="请输入内容" v-model="batch">
            <template slot="prepend">batch</template>
        </el-input>
        <el-input placeholder="请输入内容" v-model="lr">
            <template slot="prepend">lr</template>
        </el-input>
    </div>
</template>

<script>
import 'element-ui/lib/theme-chalk/index.css'
import method from './hyperparam.method'
import { createNamespacedHelpers } from 'vuex'
const {mapActions: mapDebugActions, mapGetters:mapDebugGetters} = createNamespacedHelpers('debug')
export default {
    data(){
        return {
            batch:100,
            lr:0.01
        }
    },
    computed:{
        ...mapDebugGetters(['getLr','getBatch'])
    },
    watch:{
        getLr:{
            handler(val){
                this.lr = val
            }
        },
        getBatch:{
            handler(val){
                this.batch = val
            }
        },
        batch:{
            handler(val){
                this.setBatchsize({"batchsize":parseInt(val)})
            }
        },
        lr:{
            handler(val){
                this.setLr({"lr":parseFloat(val)})
            }
        }
    },
    methods:{
        ...method,
        ...mapDebugActions(['setLr','setBatchsize'])
        
    }
}
</script>

<style lang="less" scoped>
@import 'hyperparam.less';
</style>

