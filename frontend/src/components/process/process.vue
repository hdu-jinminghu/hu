<template>
    <div :class="['process-container']">
        <div :class="['title','build','activep']" @click="changePanel('build')"> BUILD </div>
        <div :class="['big-triangle','build-btri']">
            <div :class="['small-triangle','build-stri','activep-tri']"></div>
        </div>
        <div :class="['title','debug']" @click="changePanel('debug')"> DEBUG </div>
        <div :class="['big-triangle','debug-btri']">
            <div :class="['small-triangle','debug-tri','debug-stri']"></div>
        </div>
         <div :class="['title','test']" @click="changePanel('test')"> TEST </div>
    </div>
</template>

<script>
import methods from './process.method'
export default {
    data:function(){
        return{
            process:{'build':'/index/Build','debug':'/index/Debug','test':'/index/Test'},
            eles:{'build':['build','build-stri'],'debug':['debug','debug-stri','build-btri'],'test':['test','debug-btri']}
        }
    },
    methods:{
        ...methods
    }
}
</script>

<style lang="less" scoped>
@import 'process.less';
</style>