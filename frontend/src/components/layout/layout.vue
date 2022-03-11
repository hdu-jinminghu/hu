<template>
    <div :class="['layout']">
        <div :class="['head']"></div>
        <div :class="['body']">
            <div :class="['model-view']">
                <model-view></model-view>
            </div>
            <div :class="['panel']">
                <div :class="['process']">
                    <Process/>
                </div>
                <div :class="['content']">
                    <keep-alive>
                        <router-view></router-view>
                    </keep-alive>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import methods from './layout.method'
import modelView from './modelView/modelView'
import { createNamespacedHelpers } from 'vuex'
import Process from '../process/process'
const {mapMutations: mapLayoutMutations} = createNamespacedHelpers('layout')
export default {
    data(){
        return {
        }
    },
    components:{
        modelView,
        Process
    },
    mounted(){
        this.init()
    },
    methods:{
        ...methods,
    }
}
</script>

<style lang="less" scoped>
@import 'layout.less';
</style>