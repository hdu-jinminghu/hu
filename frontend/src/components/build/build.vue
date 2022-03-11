<template>
    <div class="nodes-wrap">
        <div :class="['build-selector-group']">
            <hyper></hyper>
        </div>
        <div :class="['build-subdivide-head-card']" @click="layerShow=!layerShow">
            <div :class="['build-subdivide-head']">
                layer
            </div>
            <div :class="['build-subdivide-head-tail']">
            </div>
        </div>
        <div :class="['node-container']" v-if="layerShow">
            <div v-for="item in layerNodeList" :key="item.type" class="node" draggable="true" @dragstart="drag($event, item)" :class="[item.typeName]">
                <div class="name">{{item.typeName}}</div>
            </div>
        </div>
        <div :class="['build-subdivide-head-card']" @click="opShow=!opShow">
            <div :class="['build-subdivide-head']">
                op
            </div>
            <div :class="['build-subdivide-head-tail']">
            </div>
        </div>
        <div :class="['node-container']" v-if="opShow">
            <div v-for="item in opNodeList" :key="item.type" class="node" draggable="true" @dragstart="drag($event, item)" :class="[item.typeName]">
                <div class="name">{{item.typeName}}</div>
            </div>
        </div>
        <div :class="['build-subdivide-head-card']" @click="moduleShow=!moduleShow">
            <div :class="['build-subdivide-head']">
                module
            </div>
            <div :class="['build-subdivide-head-tail']">
            </div>
        </div>
        <div :class="['node-container']" v-if="moduleShow">
            <template v-for="ce in Object.keys(getModuleCe)">
                <div :class="['build-subdivide-card']" :key="ce">
                    <div :class="['divider']" @click="selectModule(ce)">
                        <div :class="['divider__text']" :id="ce">
                            {{ce}}
                            <i :class="['build-component-select']"/>
                        </div>
                        
                        <!-- <div :class="['build-component-select']" :id="ce" @click="selectModule(ce)">
                            <i/>
                        </div> -->
                    </div>
                    <div :class="['build-subdivide-content-card']">
                        <div v-for="item in isshow(getModuleCe[ce])" :key="getModuleList[item].type" class="node" draggable="true" @dragstart="drag($event, getModuleList[item])" @dblclick="reload($event)" @click="showctrol(item)">
                            <div :class="['build-module-outer']" >
                                <div :class="{name:isActive(item),namekid:!isActive(item)}">{{item}}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
            <div :class="['build-subdivide-card']" :key="'automl'">
                <div :class="['divider']" @click="selectModule('automl')">
                    <div :class="['divider__text']" :id="'automl'">
                        automl
                        <i :class="['build-component-select']"/>
                    </div>
                </div>
                <div :class="['build-subdivide-content-card']">
                    
                    <div v-for="item in autoMlModules" :key="item.type" class="node autoM" draggable="true" @dragstart="drag($event, item)">
                        
                            <div class="name">{{item.type}}</div>
                            <div class="autoAttrs">
                                <div>D:{{item.attrs.deepth}}</div>
                                <div>C:{{item.attrs.channels}}</div>
                            </div>
                        
                    </div>
                    <div :key="'addModuleButton'" class="node" style="cursor:auto" @click="autoDialogFormVisible=true">
                            <i class="el-icon-plus" style="margin:auto;fontSize:20px"></i>
                    </div>
                </div>
            </div>
        </div>
        <div :class="['build-subdivide-head-card']" @click="modelShow=!modelShow">
            <div :class="['build-subdivide-head']">
                model
            </div>
            <div :class="['build-subdivide-head-tail']">
            </div>
        </div>
        <div :class="['listPanel']" v-if="modelShow">
            <listPanle></listPanle>
        </div>
        <!-- <div :class="['build-subdivide-head-card']" @click="modelAttrs=!modelAttrs">
            <div :class="['build-subdivide-head']">
                attrs
            </div>
            <div :class="['build-subdivide-head-tail']">
            </div>
        </div> -->
        <keep-alive>
            <div :class="['build-attrBox']" v-if="modelAttrs">
                <attrBox></attrBox>
            </div>
        </keep-alive>
        
        <div :class="['buttons-container']">
            <ButtonList @trigerEvent='exec'></ButtonList>
        </div>
        

        <el-dialog :visible.sync="dialogFormVisible">
            <el-form :model="form">
                <el-form-item  label="模块名" :label-width="formLabelWidth">
                <el-input v-model="form.name" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
            </div>
        </el-dialog>

        <el-dialog :visible.sync="autoDialogFormVisible">
            <el-form :model="autoForm">
                <el-form-item  label="Channels" :label-width="formLabelWidth">
                <el-input v-model="autoForm.channels" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item  label="Depth" :label-width="formLabelWidth">
                <el-input v-model="autoForm.deepth" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="autoDialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="addAutoMl()">确 定</el-button>
            </div>
        </el-dialog>

    </div>
        
</template>

<script>
import { createNamespacedHelpers } from 'vuex'
const {mapMutations: mapModelViewMutations,mapGetters:mapModelViewGetters} = createNamespacedHelpers('modelView')
import methods from './build.method'
import ButtonList from './buttonList/buttonList.vue'
import listPanle from './listPanel/listPanel.vue'
import attrBox from './attrBox/attrBox.vue'
import hyper from './hyper/hyper.vue'
import {lossFcs,datasets,opNodeList,layerNodeList} from './init'
export default {
    components:{
        ButtonList,
        listPanle,
        attrBox,
        hyper
    },
    data(){
        return{
            autoDialogFormVisible:false,
            value:true,
            modelShow:true,
            moduleShow:true,
            opShow:true,
            modelAttrs:true,
            layerShow:true,
            opNodeList: opNodeList,
            layerNodeList: layerNodeList,
            moduleList:{},
            nodeTypeObj: {},
            isshowlist:[],
            isshowresnet:false,
            isshowgooglenet:false,
            resnetnum:0,
            googlenetnum:0,


            dialogFormVisible:false,
            form:{
                name:''
            },
            formLabelWidth: '120px',
            applyModule:[],
            autoMlModules:[],
            autoForm:{
                'channels':0,
                "deepth":0,
            }
        }
    },
    mounted(){
        this.initNodeTypeObj()
        
    },
    methods:{
        ...mapModelViewMutations(['setDragItem','setDir','setModuleId','setActiveModule','setApplyModule','setAutomlM']),
        ...methods,
        showctrol(key){
            if(key=="resnet50"){
                if(this.resnetnum%2==0){
                    this.isshowresnet = true
                    
                }
                else{
                    this.isshowresnet = false
                }
                this.resnetnum++
                
            }
            else if(key=="googlenet"){
                if(this.googlenetnum%2==0){
                    this.isshowgooglenet = true
                }
                else{
                    this.isshowgooglenet = false
                }
                this.googlenetnum++
                
            }
            
        }
        
    },
    watch:{
        dialogFormVisible:{
            handler(val){
                (!val) && (function(that){
                    that.setModuleId(that.form.name)
                    that.form.name != '' && 
                    (that.$nextTick(()=>{
                        that.setDir('confirm')
                    }))
                })(this)
            }
        },
        applyModule:{
            deep:true,
            handler(val){
                this.setApplyModule(val)
            }
        }
    },
    computed:{
        ...mapModelViewGetters(['getModuleList','getModuleCe']),
        isActive(){
            return function(item){
                let net = ["Lenet","Alexnet","resnet50","googlenet","vgg16"]
                if(net.includes(item)){
                    return true
                }
                else{
                    return false
                }
            }
        },
        isshow(){
            return function(needlist){
                let newlist = []
                let net = ["Lenet","Alexnet","resnet50","googlenet","vgg16"]
                let resnetlist = [
                        "resBottleNeck1"
                            ,"resBottleNeck2"
                            ,"resBottleNeck3"
                            ,"resBottleNeck4"
                            ,"resBottleNeck5"
                            ,"resBottleNeck6"
                            ,"resBottleNeck7"
                            ,"resBottleNeck8"
                    ]
                let googlenetlist = [
                    "inception3a"
                    ,"inception3b"
                    ,"inception4a"
                    ,"inception4b"
                    ,"inception4c"
                    ,"inception4d"
                    ,"inception4e"
                    ,"inception5a"
                    ,"inception5b"
                ]
                if(this.isshowresnet==false && this.isshowgooglenet==false){
     
                    for(let item of needlist){
                        if(net.includes(item)){
                            newlist.push(item)
                        }
                    }
                }
                else if(this.isshowresnet == true && this.isshowgooglenet==false){
                    for(let item of needlist){
                        if(!googlenetlist.includes(item)){
                            newlist.push(item)
                        }
                    }
                }
                else if(this.isshowgooglenet == true && this.isshowresnet==false){
                    for(let item of needlist){
                        if(!resnetlist.includes(item)){
                            newlist.push(item)
                        }
                    }
                
                }
                else if(this.isshowgooglenet == true && this.isshowresnet==true){
                    return needlist
                }
                 return newlist  
            }
        }
    }
}
</script>

<style lang="less" scoped>
@import 'build.less';
</style>