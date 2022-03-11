import { jsPlumb } from "jsplumb";
import { IDGenerator } from "./until";
import panzoom from "panzoom";
import utils from '@/utils/layout'
import * as d3 from "d3"
const GenNonDuplicateID = IDGenerator()
const methods = {
    init() {
      this.jsPlumb.ready(() => {
        // 导入默认配置
        this.jsPlumb.importDefaults(this.jsplumbSetting);
        //完成连线前的校验
        this.jsPlumb.bind("beforeDrop", evt => {
          let res = () => { } //此处可以添加是否创建连接的校验， 返回 false 则不添加； 
          return res
        })
        // 连线创建成功后，维护本地数据
        this.jsPlumb.bind("connection", evt => {
          this.addLine(evt)
        });
        //连线双击删除事件
        this.jsPlumb.bind("dblclick",(conn, originalEvent) => {
          this.confirmDelLine(conn)
        })
        //连线右键事件
        this.jsPlumb.bind("contextmenu",(conn, originalEvent) => {
          originalEvent.preventDefault()
          this.setLineAttr(conn)
        })
        //断开连线后，维护本地数据
        this.jsPlumb.bind("connectionDetached", evt => {
          this.deleLine(evt)
        })
        // 会使整个jsPlumb立即重绘。
        this.jsPlumb.setSuspendDrawing(false, true);
      });
      this.initPanZoom();
    },
    draggableNode(nodeId) {
      this.jsPlumb.draggable(nodeId, {
        grid: this.commonGrid,
        drag: (params) => {
          this.alignForLine(nodeId, params.pos)
        },
        start: () => {
  
        },
        stop: (params) => {
          this.auxiliaryLine.isShowXLine = false
          this.auxiliaryLine.isShowYLine = false
          this.changeNodePosition(nodeId, params.pos)
        }
      })
    },
    //移动节点时，动态显示对齐线
    alignForLine(nodeId, position) {
      let showXLine = false, showYLine = false
      this.graph.nodeList.some(el => {
        if(el.id !== nodeId && el.left == position[0]+'px') {
          this.auxiliaryLinePos.x = position[0] + 60;
          showYLine = true
        }
        if(el.id !== nodeId && el.top == position[1]+'px') {
          this.auxiliaryLinePos.y = position[1] + 20;
          showXLine = true
        }
      })
      this.auxiliaryLine.isShowYLine = showYLine
      this.auxiliaryLine.isShowXLine = showXLine
    },
    changeNodePosition(nodeId, pos) {
      this.graph.nodeList.some(v => {
        if(nodeId == v.id) {
          v.left = pos[0] +'px'
          v.top = pos[1] + 'px'
          return true
        }else {
          return false
        }
      })
    },
    drag(ele, item) {
      this.currentItem = item;
    },
    drop(event) {
      const containerRect = this.jsPlumb.getContainer().getBoundingClientRect();
      const scale = this.getScale();
      let left = (event.pageX - containerRect.left -60) / scale;
      let top = (event.pageY - containerRect.top -20) / scale;
      
      var temp = {
        ...this.currentItem,
        id: GenNonDuplicateID("node"),
        top: (Math.round(top/20))*20 + "px",
        left:  (Math.round(left/20))*20 + "px"
      };
      this.changeItemInfo(temp)
      this.addNode(temp);
    },
    addLine(line) {
      let from = line.source?line.source.id:line.from;
      let to = line.target?line.target.id:line.to;
      this.graph.lineList.push({
        from: from,
        to: to,
        label: "连线名称",
        id: GenNonDuplicateID("link",from,to),
        Remark: ""
      });
    },
    confirmDelLine(line) {
      this.$Modal.confirm({
        title: '删除连线',
        content: "<p>确认删除该连线？</p>",
        onOk: () => {
          this.jsPlumb.deleteConnection(line)
        }
      })
    },
    deleLine(line) {
      this.graph.lineList.forEach((item, index) => {
        if(item.from === line.sourceId && item.to === line.targetId) {
          this.graph.lineList.splice(index, 1)
        }
      })
    },
    // dragover默认事件就是不触发drag事件，取消默认事件后，才会触发drag事件
    allowDrop(event) {
      event.preventDefault();
    },
    getScale() {
      let scale1;
      if (this.jsPlumb.pan) {
        const { scale } = this.jsPlumb.pan.getTransform();
        scale1 = scale;
      } else {
        const matrix = window.getComputedStyle(this.jsPlumb.getContainer()).transform;
        scale1 = matrix.split(", ")[3] * 1;
      }
      this.jsPlumb.setZoom(scale1);
      return scale1;
    },
    // 添加新的节点
    addNode(temp) {
      this.graph.nodeList.push(temp);
      this.$nextTick(() => {
        this.jsPlumb.makeSource(temp.id, this.jsplumbSourceOptions);
        this.jsPlumb.makeTarget(temp.id, this.jsplumbTargetOptions);
        this.draggableNode(temp.id)
      });
    },
  
    initPanZoom() {
      const mainContainer = this.jsPlumb.getContainer();
      const mainContainerWrap = mainContainer.parentNode;
      const pan = panzoom(mainContainer, {
        smoothScroll: false,
        bounds: false,
        // autocenter: true,
        zoomSpeed: 0.065,
        zoomDoubleClickSpeed: 1,
        minZoom: 0.1,
        maxZoom: 5,
        //设置滚动缩放的组合键，默认不需要组合键
        beforeWheel: (e) => {
        },
        beforeMouseDown: function(e) {
          // allow mouse-down panning only if altKey is down. Otherwise - ignore
          var shouldIgnore = e.ctrlKey;
          return shouldIgnore;
        }
      });
      this.jsPlumb.mainContainerWrap = mainContainerWrap;
      this.jsPlumb.pan = pan;
      // 缩放时设置jsPlumb的缩放比率
      pan.on("zoom", e => {
        const { x, y, scale } = e.getTransform();
        this.jsPlumb.setZoom(scale);
        //根据缩放比例，缩放对齐辅助线长度和位置
        this.auxiliaryLinePos.width = (1/scale) * 100 + '%'
        this.auxiliaryLinePos.height = (1/scale) * 100 + '%'
        this.auxiliaryLinePos.offsetX = -(x/scale)
        this.auxiliaryLinePos.offsetY = -(y/scale)
      });
      pan.on("panend", (e) => {
        const {x, y, scale} = e.getTransform();
        this.auxiliaryLinePos.width = (1/scale) * 100 + '%'
        this.auxiliaryLinePos.height = (1/scale) * 100 + '%'
        this.auxiliaryLinePos.offsetX = -(x/scale)
        this.auxiliaryLinePos.offsetY = -(y/scale)
      })
  
      // 平移时设置鼠标样式
      mainContainerWrap.style.cursor = "grab";
      mainContainerWrap.addEventListener("mousedown", function wrapMousedown() {
        this.style.cursor = "grabbing";
        mainContainerWrap.addEventListener("mouseout", function wrapMouseout() {
          this.style.cursor = "grab";
        });
      });
      mainContainerWrap.addEventListener("mouseup", function wrapMouseup() {
        this.style.cursor = "grab";
      });
    }, 
  
    setNodeName(nodeId, name) {
      this.graph.nodeList.some((v) => {
        if(v.id === nodeId) {
          v.nodeName = name
          return true
        }else {
          return false
        }
      })
    },
  
    //删除节点
    deleteNode(node) {
      this.graph.nodeList.some((v,index) => {
        if(v.id === node.id) {
          this.graph.nodeList.splice(index, 1)
          this.jsPlumb.remove(v.id,true)
          return true
        }else {
          return false
        }
      })
    },
    changInfo:function(node){
      this.changeItemInfo(node)
    },
  
    //更改连线状态
    changeLineState(nodeId, val) {
      let lines = this.jsPlumb.getAllConnections()
      lines.forEach(line => {
        if(line.targetId === nodeId || line.sourceId === nodeId) {
          if(val) {
            line.canvas.classList.add('active')
          }else {
            line.canvas.classList.remove('active')
          }
        }
      })
    },
    cancelConnect(clearExplore=true){
      let lineList = this.jsPlumb.getAllConnections()
      let lineList_ = JSON.parse(JSON.stringify(this.graph.lineList))
      
      for(let line of lineList){
        this.jsPlumb.deleteConnection(line)
      }
      for(let node of this.graph.nodeList){
        this.jsPlumb.remove(node.id)
      }
      this.graph.lineList.push(...lineList_)
      if(clearExplore){
        let l = this.exploreStage.length
        this.exploreStage.splice(0,l)
        this.stages.splice(1,l)
      }
      this.graph = {"lineList":[],"nodeList":[]}
    },
    reload(val,clearExplore=true){
      this.cancelConnect(clearExplore)
      this.$nextTick(()=>{
        window.jsPlumb.Defaults.env = "adjust";
        // this.graph.lineList = JSON.parse(JSON.stringify(val.lineList))
        this.graph.lineList = val.lineList
        for(let node of val.nodeList){
          this.addNode(node)
        }
        this.graph.nodeList = val.nodeList
        this.$nextTick(()=>{
          this.jsPlumb.unbind("connection"); //取消连接事件
          for (let i = 0; i < val.lineList.length; i++) {
            let line = val.lineList[i];
            this.jsPlumb.connect(
              {
                source: line.from,
                target: line.to
              },
              this.jsplumbConnectOptions
            );
          }
          this.jsPlumb.bind("connection", evt => {
            let from = evt.source.id;
            let to = evt.target.id;
            this.graph.lineList.push({
              from: from,
              to: to,
              label: "连线名称",
              id: GenNonDuplicateID("link",from,to),
              Remark: ""
            });
          });
          window.jsPlumb.Defaults.env = "default";
        })
      })
    },
    showInfo(e){
      // console.log(e)
    },
    findAllNodes(tl,br){
      let res = {}
      res["nodeList"] = [] //
      res["lineList"] = [] //
      let store = [] // 
      let indegree = new Set() // 0入度点
      let outdegree = new Set() // 0出度点
      for(let node of this.graph.nodeList){
        let nodet = parseFloat(node["top"])
        let nodel = parseFloat(node["left"])
        if(tl[0]<=nodel && nodel<=br[0] && tl[1]<=nodet && nodet<=br[1]){
          res["nodeList"].push(node)
          store.push(node.id)
          indegree.add(node.id)
          outdegree.add(node.id)
        }
      }
  
      for(let line of this.graph.lineList){
        if(store.indexOf(line.to)>=0 && store.indexOf(line.from)>=0){
          res["lineList"].push(line)
          if(indegree.has(line.to)){
            indegree.delete(line.to)
          }
          if(outdegree.has(line.from)){
            outdegree.delete(line.from)
          }
        }
      }
  
      if(indegree.size == 1 && outdegree.size == 1){
        let innode = Array.from(indegree.values())[0]
        let outnode = Array.from(outdegree.values())[0]
        for(let node of res["nodeList"]){
          if(node.id == innode) {
            if(node.type != "input") {
              let newNode = {}
              newNode["id"] = GenNonDuplicateID("node")
              newNode["left"] = `${tl[0]}px`
              newNode["top"] = `${tl[1]}px`
              newNode["attrs"] = {}
              newNode["log_bg_color"] = "rgba(0, 128, 0, 0.2)"
              newNode["nodeName"] = "input"
              newNode["type"] = "input"
              newNode["typeName"] = "input"
              res["nodeList"].push(newNode)
              res["lineList"].push({
                from: newNode["id"],
                to: node["id"],
                label: "连线名称",
                id: GenNonDuplicateID("link",newNode["id"],node["id"]),
                Remark: ""
              })
            }
          }
          if(node.id == outnode) {
            if(node.type != "output") {
              let newNode = {}
              newNode["id"] = GenNonDuplicateID("node")
              newNode["left"] = `${br[0]}px`
              newNode["top"] = `${br[1]}px`
              newNode["attrs"] = {}
              newNode["log_bg_color"] = "rgba(0, 128, 0, 0.2)"
              newNode["nodeName"] = "output"
              newNode["type"] = "output"
              newNode["typeName"] = "output"
              res["nodeList"].push(newNode)
              res["lineList"].push({
                from: node["id"],
                to: newNode["id"],
                label: "连线名称",
                id: GenNonDuplicateID("link",node["id"],newNode["id"]),
                Remark: ""
              })
            }
          }
        }
      }
      return res
    },
    changeConfig(option){
      if(option == "default"){
        this.jsplumbSetting = this.jsplumbSettingDefault;
        this.jsplumbConnectOptions = this.jsplumbConnectOptionsDefault;
        this.jsplumbSourceOptions = this.jsplumbSourceOptionsDefault;
        this.jsplumbTargetOptions = this.jsplumbTargetOptionsDefault;
      } else {
        this.jsplumbSetting = this.jsplumbSettingAdjust;
        this.jsplumbConnectOptions = this.jsplumbConnectOptionsAdjust;
        this.jsplumbSourceOptions = this.jsplumbSourceOptionsAdjust;
        this.jsplumbTargetOptions = this.jsplumbTargetOptionsAdjust;
      }
    },
    adjustLayout(){
      let graph = JSON.parse(JSON.stringify(this.graph));
      utils.layout(graph);
      window.jsPlumb.Defaults.env = "adjust";
      this.$nextTick(()=>{
        this.reload(graph);
      })
    },
    setModule(){
      let graph = JSON.parse(JSON.stringify(this.graph));
      this.setModuleData(graph)
    },
    backstep(){
      if(this.exploreStage.length == 0){
        return
      } else {
        let graph = this.exploreStage.pop()
        let l = this.stages.length
        this.stages.splice(l-1,1)
        this.reload(graph,false)
      }
    },
    explore(graph){
      this.exploreStage.push(this.graph)
      let l = this.stage.length
      this.stages.splice(l,0,graph.id)
      utils.layout(graph)
      this.reload(graph,false)
    },
    // ctrl + 左键 初始化刷子 layerX不稳定
    setInitMousePos(e){
      this.env["ctrl"] && (function(that){
        that.initX = parseFloat(e.clientX)
        that.initY = parseFloat(e.clientY)  - 40
        let bias = d3.select("#flow").style("transform")

        var patt=/-?[0-9]+(\.?[0-9]+)?/g
        let comp = bias.match(patt)
        let scale = parseFloat(comp[0])
        let TOP = (that.initY - parseFloat(comp[5]))/scale
        let LEFT = (that.initX - parseFloat(comp[4]))/scale
        d3.select(".brush").style("top",`${TOP}px`).style("left",`${LEFT}px`).style('visibility',"visible")
      })(this)
      this.env["click"] = true
    },
    getMousePos(e){
      this.env["ctrl"] && this.env["click"] && (function(that){
        that.endX = parseFloat(e.clientX)
        that.endY = parseFloat(e.clientY) - 40
        let bias = d3.select("#flow").style("transform")

        var patt=/-?[0-9]+(\.?[0-9]+)?/g
        let comp = bias.match(patt)
        let scale = parseFloat(comp[0])
        d3.select(".brush").style("height",`${Math.abs(that.initY - that.endY)/scale}px`)
                            .style("width",`${Math.abs(that.initX - that.endX)/scale}px`)
      })(this)
    },
    setEnv(e){
      e.code == 'ControlLeft' && (this.env["ctrl"] = true)
      e.code == 'KeyV' && (this.env["KeyV"] = true)
    },
    // 组合按键
    releaseMouse(){
      this.env["click"] = false
    },
    releaseEnv(e){
      e.code == 'ControlLeft' && (this.env["ctrl"] = false)
      e.code == 'KeyV' && (this.env["KeyV"] = false)
    },
    // 重置刷子
    resetBrush(){
      d3.select('.brush').style("height",`0px`)
      .style("width",`0px`).style('visibility',"hidden")
    },
    // 节点过滤
    setSelected(){
      let itemArray = d3.selectAll('.node-item').nodes()
      let brush = d3.select(".brush")
      let scope = [parseFloat(brush.style("top")),parseFloat(brush.style("left")),
      parseFloat(brush.style("top"))+parseFloat(brush.style("height")),parseFloat(brush.style("left"))+parseFloat(brush.style("width"))]
      if(scope[0] == scope[2] && scope[1] == scope[3]){
        return
      }
      this.selectedItem.splice(0,this.selectedItem.length)
      d3.selectAll(".node-item-selected").classed("node-item-selected",false)
      itemArray.forEach((item)=>{
        let e = item;
        let height = parseFloat(d3.select(e).style("height"));
        let width = parseFloat(d3.select(e).style("width"));
        let top = parseFloat(d3.select(e).style("top"));
        let left = parseFloat(d3.select(e).style("left"));
        ((scope[0]<top && top<scope[2] && scope[1]<left && left<scope[3]) ||
        (scope[0]<top+height && top+height<scope[2] && scope[1]<left && left<scope[3]) ||
        (scope[0]<top+height && top+height<scope[2] && scope[1]<left+width && left+width<scope[3])||
        (scope[0]<top && top<scope[2] && scope[1]<left+width && left+width<scope[3])) && 
        (function(that){
            that.selectedItem.push(d3.select(e).attr("id"));
            d3.select(e).classed("node-item-selected",true);
          })(this);
      })
      this.$nextTick(()=>{
        this.resetBrush();
      })
    },
    postAutoMlRough(form){
      let params = {...form}
      let graph = this.graph
      if(this.exploreStage.length > 0){
        graph = this.exploreStage[0]
      }
      params['selectArea'] = this.selectedItem
      params["graph"] = graph
      this.setModelSData([this.modelName,graph,this.lossFc,this.dataset])
      this.$nextTick(()=>{
        this.roughAutoml(params)
      })
    },
    // 查找剪枝网络层
    targetLayer(vertex){
      let baseLayer = ["conv2d",'bn2d','relu','maxpool2d']
      let topo = {}
      for(let line of this.graph["lineList"]){
        if(line["from"] in topo){
          topo[line["from"]].push(line["to"])
        } else {
          topo[line["from"]] = [line["to"]]
        }
        if(! (line["to"] in topo)){
          topo[line["to"]] = []
        }
      }
      let v = vertex.id
      let sequence = []


      while(true){
        if(topo[v].length == 1){
          sequence.push(topo[v][0])
          v = topo[v][0]
        } else{
          break
        }
      }

      let target = {
        "conv1":undefined,
        'bn2d':undefined,
        'conv2':undefined
      }
      let targetVertex = {
        "conv1":vertex,
        'bn2d':undefined,
        'conv2':undefined
      }
      target['conv1'] = vertex.id
      let finisTag = false
      for(let u of sequence){
        if(finisTag){
          break
        }
        for(let node of this.graph["nodeList"]){
          if(node.id == u){
            if(baseLayer.includes(node.type)){
              if(node.type == "bn2d"){
                target['bn2d'] = node.id
                targetVertex["bn2d"] = node
              } else if(node.type == "conv2d"){
                target['conv2'] = node.id
                targetVertex["conv2"] = node
                finisTag = true
                break
              }
            } else {
              finisTag = true
            }
          }
        }
      }
      if(target["conv2"] == undefined){
        this.$message("不支持剪枝")
      } else{
        for(let type in target){
          if(target[type]){
            let id = `${this.stage}/${target[type]}`
            let id_ = id.split("/")
            id_.splice(0,1)
            
            target[type] = '*' + id_.join('*')
          }
        }
      }
      this.set_prun_target(target)
      this.set_prun_targetVertex(targetVertex)
    },
    duplicate:function(){
      let outLine = []  //  出边
      let inLine = [] //  入边
      let lineList = []  //  内部边
      let topoGraph = []
      let entry = undefined  // 入口
      let exit = undefined  //  出口
      for(let line of this.graph['lineList']){
        if(this.selectedItem.includes(line["from"])){
          outLine.push(line)
        }
        if(this.selectedItem.includes(line["to"])){
          inLine.push(line)
        }
        if(this.selectedItem.includes(line["to"]) && this.selectedItem.includes(line["from"])){
          lineList.push(line)
        }
      }

      //  查找出口
      for(let line of outLine){
        if(this.selectedItem.includes(line["to"])){
          continue
        } else {
          exit = line
          break
        }
      }
      //  查找入口
      for(let line of inLine){
        if(this.selectedItem.includes(line["from"])){
          continue
        } else {
          entry = line
          break
        }
      }
      //  模板
      let template = {"lineList":[],"nodeList":[]} 
      template["lineList"] = lineList
      for(let vertex of this.graph['nodeList']){
        if(this.selectedItem.includes(vertex["id"])){
          template["nodeList"].push(vertex)
        }
      }
      // 生成重复模块
      let insertModule = []
      for(let i=0;i<this.duplicateTimes;i++){
        let nModule = JSON.parse(JSON.stringify(template))
        let lineList = nModule['lineList']
        let nodeList = nModule['nodeList']
        for(let j in lineList){
          let line = lineList[j]
          line['from'] = `${line['from']}O${this.duplicateOp}d${i}`
          line['to'] = `${line['to']}O${this.duplicateOp}d${i}`
        }
        for(let j in nodeList){
          let node = nodeList[j]
          node['id'] = `${node['id']}O${this.duplicateOp}d${i}`
        }

        insertModule.push(nModule)
      }
      // 插入结构数据
      for(let i in insertModule){
        let module = insertModule[i]
        this.graph['lineList'] = [...this.graph['lineList'],...module['lineList']]
        this.graph['nodeList'] = [...this.graph['nodeList'],...module['nodeList']]
        let from = exit["from"]
        let to = `${entry["to"]}O${this.duplicateOp}d${i}`
        if(i !=0 ){
          from = `${from}O${this.duplicateOp}d${i-1}`
        }
        
        this.graph['lineList'].push({"from":from,"to":to})
        // console.log({"from":from,"to":to})
        if(i == (insertModule.length-1)){
          this.graph['lineList'].push({"from":`${exit["from"]}O${this.duplicateOp}d${i}`,"to":exit["to"]})
          // console.log({"from":`${from}d${i}`,"to":exit["to"]})
        }

        // console.log({"from":from,"to":to})
      }
      // console.log(this.graph['lineList'])
      // 重新绘制
      // console.log(exit,entry)
      this.$nextTick(()=>{
        for(let i in this.graph['lineList']){
          if(this.graph['lineList'][i]["from"] == exit["from"] && this.graph['lineList'][i]["to"] == exit["to"]){
            this.graph['lineList'].splice(i,1)
            break
          }
        }
      })
      
      this.$nextTick(()=>{
        this.adjustLayout()
      })
      this.duplicateOp += 1
    }
  }

export default methods;