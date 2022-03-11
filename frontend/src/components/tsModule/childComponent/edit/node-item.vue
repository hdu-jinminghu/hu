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
    <div class="nodeName">{{node.nodeName}}</div>
    <div v-if="cbf" class="nodeAttr">{{attr}}</div>
      <!--连线用--//触发连线的区域-->
      <div class="node-anchor anchor-top" v-show="mouseEnter"></div>
      <div class="node-anchor anchor-right" v-show="mouseEnter"></div>
      <div class="node-anchor anchor-bottom" v-show="mouseEnter"></div>
      <div class="node-anchor anchor-left" v-show="mouseEnter"></div>
  </div>
</template>

<script>
import ClickOutside from 'vue-click-outside'
export default {
  name: "nodeItem",
  props: {
      node: Object
  },
  directives: {
    ClickOutside
  },
  computed: {
    // 节点容器样式
    flowNodeContainer: {
      get() {
        return {
          top: this.node.top,
          left: this.node.left,
          attr:'',
        };
      }
    }
  },
  data() {
    return {
      mouseEnter: false,
      isActive: false,
      isSelected: false,
      cbf:false,
      attr:''
    };
  },
  watch:{
    node:{
      immediate: true,
      deep:true,
      handler(val){
        if(val.typeName.startsWith("bn")){
          this.attr = `features:[${val.attrs["num_features"]}]`
          this.cbf = true
        }
        if(val.typeName.startsWith("conv")){
          this.attr = `kernel:[${val.attrs["out_channels"]},${val.attrs["in_channels"]},${val.attrs["kernel_size"]},${val.attrs["kernel_size"]}]`
          this.cbf = true
        }
        if(val.typeName.startsWith("linear")){
          this.attr = `kernel:[${val.attrs["in_features"]},${val.attrs["out_features"]}]`
          this.cbf = true
        }
      }
    }
  },
  methods: {
    showAnchor() {
      this.mouseEnter = true
      setTimeout(() => {
        this.$emit("showInfo", this.node)
      },0)
    },
    hideAnchor() {
      this.mouseEnter = false
    },
    onContextmenu() {
      this.$contextmenu({
        items: [{
          label: '删除',
          disabled: false,
          icon: "",
          onClick: () => {
            this.deleteNode()
          }
        },{
          label: '修改',
          disabled: false,
          icon: "",
          onClick:()=>{
            setTimeout(() => {
              this.$emit("changInfo", this.node)
            },0)
          }
        }],
        event,
        customClass: 'custom-class',
        zIndex: 9999,
        minWidth: 180
      })
    },
    setActive() {
      if(window.event.ctrlKey){
        this.isSelected = !this.isSelected
        return false
      }
      this.isActive = true
      this.isSelected = false
      setTimeout(() => {
        this.$emit("changeLineState", this.node.id, true)
      },0)
    },
    setNotActive() {
      if(!window.event.ctrlKey){
        this.isSelected = false
      }
      if(!this.isActive) {
        return
      }
      this.$emit("changeLineState", this.node.id, false)
      this.isActive = false
    },
    editNode() {
      return
    },
    deleteNode() {
      this.$emit("deleteNode", this.node)
    }
  }
};
</script>

<style lang="less" scoped>
@labelColor: #409eff;
@nodeSize: 20px;
@viewSize: 10px;
.node-item {
  position: absolute;
  display: flex;
  flex-direction: column;
  height: 40px;
  width: 120px;
  justify-content: center;
  align-items: center;
  border: 1px solid #b7b6b6;
  border-radius: 4px;
  cursor: move;
  box-sizing: content-box;
  z-index: 9995;
  &:hover {
    z-index: 9998;
    .delete-btn{
      display: block;
    }
  }
  .log-wrap{
    width: 40px;
    height: 40px;
    border-right: 1px solid  #b7b6b6;
  }
  .nodeName {
    flex-grow: 1;
    height: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .nodeAttr{
    flex-grow: 1;
    height: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .node-anchor {
    display: flex;
    position: absolute;
    width: @nodeSize;
    height: @nodeSize;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    cursor: crosshair;
    z-index: 9999;
    background: -webkit-radial-gradient(sandybrown 10%, white 30%, #9a54ff 60%);
  }
  .anchor-top{
    top: calc((@nodeSize / 2)*-1);
    left: 50%;
    margin-left: calc((@nodeSize/2)*-1);
  }
  .anchor-right{
    top: 50%;
    right: calc((@nodeSize / 2)*-1);
    margin-top: calc((@nodeSize / 2)*-1);
  }
  .anchor-bottom{
    bottom: calc((@nodeSize / 2)*-1);
    left: 50%;
    margin-left: calc((@nodeSize / 2)*-1);
  }
  .anchor-left{
    top: 50%;
    left: calc((@nodeSize / 2)*-1);
    margin-top: calc((@nodeSize / 2)*-1);
  }
}
.active{
  border: 1px dashed @labelColor;
  box-shadow: 0px 5px 9px 0px rgba(0,0,0,0.5);
}
</style>