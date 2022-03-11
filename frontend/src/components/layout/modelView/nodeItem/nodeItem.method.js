import {BASICTYPE} from '../init'
const method = {
    showAnchor() {
        this.mouseEnter = true
        console.log(this.node.id)
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
            },{
                label: '探索',
                disabled: false,
                icon: "",
                onClick:()=>{
                    if(this.node.nodeList){
                        setTimeout(() => {
                            this.$emit("explore", this.node)
                        },0)
                    } else {
                        this.$message('基础节点');
                    }
                }
            },{
                label: '剪枝',
                disabled: false,
                icon: "",
                onClick:()=>{
                    if(this.node.type != 'conv2d'){
                        this.$message('不是卷积层')
                    } else {
                        this.$emit("targetLayer", this.node)
                        this.setInitData({"Id":this.node.id,"appendix":JSON.stringify([])})
                    }
                }
            },{
                label: '批修改',
                disabled: false,
                icon: "",
                onClick:()=>{
                    this.triggerTag = true;
                    this.$emit("batchChannel")
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
    },
    batchMChannels(channels){
        // 判断是否基础节点
        if(BASICTYPE.includes(this.node.type)){
            this.$message("基础节点")
            return
        }

        // 建立字典nodeDic方便后续按节点查找
        let nodeDic = {}
        // 建立连接图
        let forwardGraph = {}
        let backwardGraph = {}

        for(let node of this.node["nodeList"]){
            nodeDic[node['id']] = node
        }
        for(let line of this.node["lineList"]){
            if(line["from"] in forwardGraph){
                forwardGraph[line["from"]].push(line["to"])
            } else  {
                forwardGraph[line["from"]] = [line["to"]]
            }

            if(!(line["to"] in forwardGraph)){
                forwardGraph[line["to"]] = []
            }


            if(line["to"] in backwardGraph){
                backwardGraph[line["to"]].push(line["from"])
            } else  {
                backwardGraph[line["to"]] = [line["from"]]
            }

            if(!(line["from"] in backwardGraph)){
                backwardGraph[line["from"]] = []
            }
        }
        // 所有节点
        let vertexs = Array.from(Object.keys(nodeDic))
        // 查找入口、出口
        let entry = undefined
        let exit = undefined
        // 模块节点
        let mVertex = []
        // 出口
        for(let uid in forwardGraph){
            if(forwardGraph[uid].length == 0){
                exit = uid
                break
            }
        }
        // 入口
        for(let uid in backwardGraph){
            if(backwardGraph[uid].length == 0){
                entry = uid
                break
            }
        }
        // 模块
        for(let uid in nodeDic){
            (BASICTYPE.includes(nodeDic[uid].type) && nodeDic[uid].type != "op_cat") || 
            (mVertex.push(uid))
        }
        // 不改out_channels：1、后面是模块；2、出口；3、后面是op_cat
        // 不改in_channels:1、前面是模块；2、入口；3、前面是op_cat
        let fixed_out = []
        let fixed_in = []

        let nextConv = function(u,arr,graph){
            let tra  =[u]
            while(tra.length > 0){
                if(nodeDic[tra[0]].type != "conv2d"){
                    tra = [...tra,...graph[tra[0]]]
                }
                arr.push(tra.shift())
            }
        }
        nextConv(exit,fixed_out,backwardGraph)
        nextConv(entry,fixed_in,forwardGraph)
        for(let v of mVertex){
            nextConv(v,fixed_out,backwardGraph)
            nextConv(v,fixed_in,forwardGraph)
        }

        // 查找fix_out、fix_in交集
        let intersection = []
        fixed_in.forEach((v)=>{
            fixed_out.includes(v) && 
            (intersection.push(v))
        })

        // all和fix_in、fix_out、intersection差集
        let rest = []
        vertexs.forEach((v)=>{
            (fixed_in.includes(v) || fixed_out.includes(v)) ||
            (rest.push(v))
        })

        // 修改channels
        for(let v of rest){
            nodeDic[v]["type"] == "bn2d" &&
            (nodeDic[v]["attrs"]["num_features"] = channels);

            nodeDic[v]["type"] == "conv2d" &&
            (nodeDic[v]["attrs"]["out_channels"] = channels) &&
            (nodeDic[v]["attrs"]["in_channels"] = channels)
        }

        for(let v of fixed_in){
            if(intersection.includes(v)){
                continue
            }
            nodeDic[v]["type"] == "conv2d" &&
            (nodeDic[v]["attrs"]["out_channels"] = channels)
        }

        for(let v of fixed_out){
            if(intersection.includes(v)){
                continue
            }
            nodeDic[v]["type"] == "conv2d" &&
            (nodeDic[v]["attrs"]["in_channels"] = channels)
        }

        this.triggerTag = false
    }
}

export default method;