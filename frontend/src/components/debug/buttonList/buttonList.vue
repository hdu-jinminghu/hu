<template>
    <div :class="['buttonContainer']" @click="triger($event)">
        <el-button-group>
            <el-button type="info" icon="el-icon-video-pause" size="mini">stop</el-button>
            <el-button type="danger" icon="el-icon-delete" size="mini">save</el-button>
            <el-button type="primary" icon="el-icon-upload" size="mini">continue</el-button>
            <el-button type="success" icon="el-icon-check" size="mini">run</el-button>
        </el-button-group>
    </div>
</template>
<script>
import 'element-ui/lib/theme-chalk/index.css'
import method  from './buttonList.method'
export default {
    data(){
        return{
            buttonTypeMap:{'el-icon-check':'run','el-button--success':'run','el-icon-delete':'save','el-button--danger':'save',
            'el-icon-upload':'continue','el-button--primary':'continue','el-icon-video-pause':"stop",'el-button--info':'stop'}
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