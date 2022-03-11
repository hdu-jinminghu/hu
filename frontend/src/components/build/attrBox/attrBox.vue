<template>
    <!-- <div :class="['attr-box']">
        <div :class="['layer-type']">{{nodeAttr['type']}}</div>
        <template v-for="attr in Object.keys(nodeAttr['attrs'])">
            <div :key="`${nodeAttr['type']}-${attr}`" :class="['attr-item']">
                <div :class="['attr-title']">{{attr}}</div>
                <el-input v-model="nodeAttr['attrs'][attr]" placeholder="请输入内容" :class="['attr-text-box']"></el-input>
            </div>
        </template>
    </div> -->

    <div>
        <el-dialog title="Attrs" :visible.sync="dialogFormVisible">
            <el-form>
                <!-- <el-form-item label="活动名称" :label-width="formLabelWidth">
                <el-input v-model="form.name" autocomplete="off"></el-input>
                </el-form-item> -->
                <template v-for="attr in Object.keys(nodeAttr['attrs'])">
                    <!-- <div :key="`${nodeAttr['type']}-${attr}`" :class="['attr-item']">
                        <div :class="['attr-title']">{{attr}}</div>
                        <el-input v-model="nodeAttr['attrs'][attr]" placeholder="请输入内容" :class="['attr-text-box']"></el-input>
                    </div> -->
                    <el-form-item :label="attr" :label-width="formLabelWidth" :key="`${nodeAttr['type']}-${attr}`">
                        <el-input v-model="nodeAttr['attrs'][attr]" autocomplete="off"></el-input>
                    </el-form-item>
                </template>
                
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex'
const {mapGetters: mapModelViewGetters} = createNamespacedHelpers('modelView')
export default {
    data(){
        return{
            nodeAttr:{'type':'','attrs':{}},
            dialogFormVisible:false,
            formLabelWidth: '120px',
        }
    },
    watch:{
        getChangeItem:function(val){
            for(let attr in val['attrs']){
                if(typeof val['attrs'][attr] === "boolean"){
                    if(val['attrs'][attr]){
                        val['attrs'][attr] = "true"
                    } else {
                        val['attrs'][attr] = "false"
                    }
                }
            }
            this.nodeAttr = val
            this.$nextTick(()=>{
                this.dialogFormVisible = true
            })
        }
    },
    computed:{
        ...mapModelViewGetters(['getChangeItem'])
    }
}
</script>

<style lang="less" scoped>
@import 'attrBox.less';
</style>