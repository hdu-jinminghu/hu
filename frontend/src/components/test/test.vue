<template>
    <div :class="['test-view']">
        <drawer></drawer>
    </div>
</template>

<script>
import methods from './test.method'
import drawer from './drawer/drawer.vue'
export default {
    components:{
        drawer
    },
    methods:{
        ...methods
    }
}
</script>

<style lang="less" scoped>
@import 'test.less';
</style>