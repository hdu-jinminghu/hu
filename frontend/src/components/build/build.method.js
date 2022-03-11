import * as d3 from "d3"

const method = {
    drag:function(e,item){
        let item_ = JSON.parse(JSON.stringify(item))
        this.setDragItem(item_);
    },
    initNodeTypeObj() {
        this.opNodeList.map(v => {
          this.nodeTypeObj[v.type] = v
        })
        this.layerNodeList.map(v => {
            this.nodeTypeObj[v.type] = v
        })
    },
    exec(e){
        if(e == 'confirm'){
            this.dialogFormVisible = true
        } else {
            this.setDir(e)
        } 
    },
    reload(e){
        let targetItem = e.path[0]
        let ativeModule = d3.select(targetItem).property('innerHTML')
        this.setActiveModule(ativeModule)
    },
    // 设置选中模块
    selectModule(e){
        if (this.applyModule.includes(e)){
            d3.select(`#${e} i`).classed("el-icon-check",false);
            this.applyModule.splice(this.applyModule.indexOf(e),1);
        } else {
            d3.select(`#${e} i`).classed("el-icon-check",true);
            this.applyModule.push(e);
        }
    },
    // 添加搜索模块
    addAutoMl(){
        this.autoDialogFormVisible = false
        let newModule = {}
        newModule["type"] = `autoM${this.autoMlModules.length}`
        newModule["attrs"] = {"channels":this.autoForm.channels,"deepth":this.autoForm.deepth}
        newModule['nodeName'] = newModule["type"]
        newModule['typeName'] = newModule["type"]
        newModule['log_bg_color'] = 'rgba(250, 205, 81, 0.2)'
        this.$nextTick(()=>{
            this.autoMlModules.push(newModule)
            this.$nextTick(()=>{
                this.setAutomlM(this.autoMlModules)
            })
        })
    },
}

export default method;