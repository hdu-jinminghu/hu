<template>

  <div class="node-item" ref="node"
    :class="[(isActive || isSelected) ? 'active' : '']"
    :style="flowNodeContainer"
    v-click-outside="setNotActive"
    @click="setActive"
    @mouseenter="showAnchor"
    @mouseleave="hideAnchor"
    @dblclick.prevent="editNode"
    @contextmenu.prevent="onContextmenu">
    <!-- <div class="container"> -->
      <div :style="typeContainerBorder">
        <div class="nodeName" :style="typeContainer">{{node.nodeName}}</div>
      </div>
      <div v-if="cbf" class="nodeAttr">{{attr}}</div>
        <!--连线用--//触发连线的区域-->
        <div class="node-anchor anchor-top" v-show="mouseEnter"></div>
        <div class="node-anchor anchor-right" v-show="mouseEnter"></div>
        <div class="node-anchor anchor-bottom" v-show="mouseEnter"></div>
        <div class="node-anchor anchor-left" v-show="mouseEnter"></div>
        <div class="node-id" v-show="mouseEnter">id:{{node['id']}}</div>
    </div>
  <!-- </div> -->

  
</template>

<script>
import ClickOutside from 'vue-click-outside'
import method from './nodeItem.method'
import { createNamespacedHelpers } from 'vuex'
const {mapGetters:mapModelViewGetters,mapMutations:mapModelViewMutations,mapActions:mapModelViewActions} = createNamespacedHelpers('modelView')
export default {
  name: "nodeItem",
  props: {
      node: Object
  },
  directives: {
    ClickOutside
  },
  data() {
    return {
      triggerTag:false, // 菜单标记
      flowNodeContainer: {
        top: this.node.top,
        left: this.node.left,
        attr:'',
        width: "120px",
        height: "23px",
        lineHieght:"23px"
      },
      mouseEnter: false,
      isActive: false,
      isSelected: false,
      cbf:false,
      attr:'',
      typeContainer:{

      },
      bgColor:{conv:"#5FBDFF", bn:"#FFDB2D", relu:"#FF6B6B", maxpool:"#689AE9", auto:"#74C3D7", module:"#7DD34D",
                linear:"#D98F59",view:"#ACC98F",add:"#9FA04C",cat:"#9A96CD",sampling:"#52ABBB",avgpool:"#FABEBE",
                adaptiveavgpool:"#F5D6C4"},
      typeContainerBorder:{
        width:"100%",
        borderRadius: "8px",
        // backgroundColor:"white",

      }
    };
  },
  computed:{
    ...mapModelViewGetters(['getChannels']),
  },
  watch:{
    getChannels:{
      handler(val){
        this.triggerTag && (this.batchMChannels(val["channels"]))
      }
    },
    mouseEnter:{
      handler(val){
        if(val){
          this.$emit("mouseOver", `id:${this.node["id"]}`)
        } else {
          this.$emit("mouseOver", "")
        }
      }
    },
    node:{
      immediate: true,
      deep:true,
      handler(val,oldval){
        this.flowNodeContainer["top"] = val.top
        this.flowNodeContainer["left"] = val.left
        let width = 0

        if(val.typeName.startsWith("auto")){  //tmplate结点
          this.typeContainer["backgroundColor"] = this.bgColor["auto"]
          this.typeContainer["border-radius"] = "8px"
        }
        if('lineList' in val){
          this.typeContainer["backgroundColor"] = this.bgColor["module"]
          this.typeContainer["border-radius"] = "8px"
          this.typeContainer["border"] = "2px solid white"
          this.typeContainerBorder["border"] = "2px solid #5DB52D"
          this.typeContainer['height'] = "19px"
          this.typeContainer['lineHeight'] = "19px"
        }

        if(val.typeName.startsWith("bn")){
          this.attr = `features:[${val.attrs["num_features"]}]`
          this.cbf = true
          this.typeContainer["backgroundColor"] = this.bgColor["bn"]
        }
        else if(val.typeName.startsWith("conv")){
          this.attr = `kernel:[${val.attrs["out_channels"]},${val.attrs["in_channels"]},${val.attrs["kernel_size"]},${val.attrs["kernel_size"]}]`
          this.cbf = true
          this.typeContainer["backgroundColor"] = this.bgColor["conv"]
        }
        else if(val.typeName.includes("linear")){
          this.attr = `kernel:[${val.attrs["in_features"]},${val.attrs["out_features"]}]`
          this.typeContainer["backgroundColor"] = this.bgColor["linear"]
          this.cbf = true
        }
        else if(val.typeName.startsWith("relu") || val.typeName.startsWith("sigmoid") || val.typeName.startsWith("tanh")){
          this.typeContainer["backgroundColor"] = this.bgColor["relu"]
          this.typeContainer["border-radius"] = "8px"
        }
        else if(val.typeName.includes("maxpool")){
          this.typeContainer["backgroundColor"] = this.bgColor["maxpool"]
          this.typeContainer["border-radius"] = "8px"
        }
        else if(val.typeName.includes("adaptiveavgpool")){
          this.typeContainer["backgroundColor"] = this.bgColor["adaptiveavgpool"]
          this.typeContainer["border-radius"] = "8px"
        }
        else if(val.typeName.includes("avgpool")){
          this.typeContainer["backgroundColor"] = this.bgColor["avgpool"]
          this.typeContainer["border-radius"] = "8px"
        }
        else if(val.typeName.includes("linear")){
           this.typeContainer["backgroundColor"] = this.bgColor["linear"]
        }
        else if(val.typeName.includes("op_view")){
           this.typeContainer["backgroundColor"] = this.bgColor["view"]
        }
        else if(val.typeName.includes("op_add")){
           this.typeContainer["backgroundColor"] = this.bgColor["add"]
        }
        else if(val.typeName.includes("op_sampling")){
           this.typeContainer["backgroundColor"] = this.bgColor["sampling"]
        }
        else if(val.typeName.includes("op_cat")){
           this.typeContainer["backgroundColor"] = this.bgColor["cat"]
        }
        if(this.cbf){
          this.flowNodeContainer["height"] = "46px"
          this.typeContainer["textAlign"] = "start"
        }
        let widthAttr = this.attr.length - 2
        let widthType = this.node.type.length
        console.log(widthAttr,widthType,this.node.type)
        width = Math.min(Math.max(width,widthAttr,widthType),20) * 8 + 8

        this.flowNodeContainer.width = width + "px"
        if(window.jsPlumb.Defaults.env == "adjust" || val == oldval){
          this.flowNodeContainer["left"] = (160 - width)/2 + parseInt(val.left) + "px"
        }
      }
    }
  },
  methods: {
    ...method,
    ...mapModelViewActions(['setInitData']),
  }
    
};
</script>

<style lang="less" scoped>
@import 'nodeItem.less';
</style>