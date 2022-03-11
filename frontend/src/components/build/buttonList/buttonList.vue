<template>
    <div :class="['buttonContainer']" @click="triger($event)">
        <el-button-group>
            <el-button type="info" icon="el-icon-question" size="mini"></el-button>
            <el-button type="danger" icon="el-icon-delete" size="mini"></el-button>
            <el-button type="warning" icon="el-icon-search" size="mini"></el-button>
            <el-button type="success" icon="el-icon-check" size="mini"></el-button>
            <el-button type="primary" icon="el-icon-video-play" size="mini"></el-button>
        </el-button-group>
    </div>
</template>
<script>
import 'element-ui/lib/theme-chalk/index.css'
import method  from './buttonList.method'
export default {
    data(){
        return{
            buttonTypeMap:{'el-icon-check':'confirm','el-button--success':'confirm','el-icon-delete':'clear','el-button--danger':'clear',
            "el-icon-question":'info','el-button--info':'info',"el-icon-search":"search","el-button--warning":"search"}
        }
    },
    methods:{
        ...method
    }
}
</script>
<style lang="less" scoped>
@import 'buttonList.less';
</style>