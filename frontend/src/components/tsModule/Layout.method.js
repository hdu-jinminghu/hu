import * as d3 from 'd3'

const methods = {
    changePanel(){
        this.historyStyle["History-close"] = !this.historyStyle["History-close"]
        this.drawerStyle["History-close"] = !this.drawerStyle["History-close"]
    },
    editModel(){
        this.editPage = !this.editPage;
    },
    changeState() {
        this.play = !this.play
        if(this.play) {
          this.setPlayTag({"tag":"p"})
        } else {
          this.setPlayTag({"tag":"s"})
        }
    },
    setFrequence_:function(val){
        this.cycle = parseInt(this.cycle)
        if( !isNaN(this.cycle)) {
          this.setCycle({"cycle":this.cycle})
        }
    },
    setLr_:function(val){
        this.cycle = parseInt(this.cycle)
        if( !isNaN(this.cycle)) {
            this.setLr({"lr":this.lr})
        }
    },
    setBatch_:function(val){
        this.cycle = parseInt(this.cycle)
        if( !isNaN(this.cycle)) {
            this.setBatchsize({"batchsize":this.batch})
        }
    },
    setEpoch_:function(val){
        this.cycle = parseInt(this.cycle)
        if( !isNaN(this.cycle)) {
            this.setTrainCycle({"trainCycle":this.epoch})
        }
    },
    // 节点名称格式转换,用于前端
    idTransformerFrontend:function(id) {
        var id = id.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\]/g, '\\]').replace(/\[/g, '\\[').replace(/\./g, '\\.')
        return id
    },
    // 节点名称格式转换,用于后端
    idTransformer:function(id) {
        var reg = /\((.*)\)/g
        var index = reg.exec(id)
        var ids = id.split("/")
        function modify(v) {
          if (v.indexOf('[') < 0) {
            return v
          } else {
            var reg = /\[(.*)\]/g
            return reg.exec(v)[1]
          }
        }
        var nodes = ids.slice(1).map(modify)
        if(index == null) {
          return nodes.join('.')
        } else {
          return `${nodes.join('.')}(${index[1]})`
        }
        
    },
    PosAdaption:function(itemnode) {
        if (itemnode) {
          const svg = d3.select('#svg-canvas')
          const str = d3.select('#svg-canvas g').attr('transform');
          let [xCoor, yCoor] = str.substring(str.indexOf('(') + 1, str.indexOf(')')).split(',')
          const { x: xCurrent, y: yCurrent } = itemnode;
          const svgWidth = d3.select('#svg-canvas').property("scrollWidth")
          const svgHeight = d3.select('#svg-canvas').property("scrollHeight")
          xCoor = Number(svgWidth) / 2  - xCurrent;
          yCoor = Number(svgHeight) / 2 - yCurrent;
          d3.select('#svg-canvas g').attr('transform', `translate(${xCoor}, ${yCoor})`)
          const transform = d3.zoomTransform(0).translate(xCoor, yCoor);
          d3.zoom().transform(svg, transform);
        }
    },
    // 图初始位置
    initPos:function(){
        if(this.initTag){
          this.drawHistory()
          const svg = d3.select('#svg-canvas')
          const canvas = d3.select('#svg-canvas')['_groups'][0][0]
          const canvasHeight = canvas.scrollHeight
          const canvasWidth = canvas.scrollWidth

          // 获取图宽、高
          const graph = d3.select('#svg-canvas g')['_groups'][0][0]
          const graphHeight = graph.getBBox().height
          const graphWidth = graph.getBBox().width

          d3.select('#svg-canvas g').attr('transform', 'translate(' + (canvasWidth - graphWidth) / 2 + ',' + (canvasHeight - graphHeight) / 2 + ')')

          // 设定zoom的初始位置
          const transform = d3.zoomTransform(0).translate((canvasWidth - graphWidth) / 2, (canvasHeight - graphHeight) / 2)
          d3.zoom().transform(svg, transform)
          this.initTag = false
        }
        d3.select(".Graph").selectAll("rect").attr("fill","#fff").attr("stroke","#000")
    },
    // structure文件内节点名与kernel_size文件内一致
    labelTransformer:function(label){
        const patt = /\[[^\/]*\]/g
        var res = label.match(patt)
        if(res != null){
          var id = res.join(".")
          id = id.replace(/\]/g,"").replace(/\[/g,"")
        }
        return id
    },
}

export default methods
