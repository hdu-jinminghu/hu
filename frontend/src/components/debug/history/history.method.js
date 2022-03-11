import * as d3 from 'd3'

const method = {
    // 在父节点parentVertex添加子节点vertex
    addVertex:function(vertex){
        let parentVertex = this.currentItemTarget
        let pos = parentVertex['pos']
        let px = pos[0]
        let py = pos[1]
        
        let x = px
        let y = py + 1
        
        let x_offset = `${150*x + 50}px`
        let y_offset = `${120*y + 20}px`

        // vertex = {'op':'test','attrs':{'acc':0,'loss':0,'lr':0,'batch':0,'step':0}}
        let ancestor = `${parentVertex['ancestor']}/${this.modelAmount}`
        let newVertex = {'uid':`item_${this.modelAmount}`,'ancestor':ancestor,'top':y_offset,'left':x_offset,'op':vertex['op'],'child':[],'pos':[x,y],'attrs':vertex['attrs']}
        // TODO 计算位置
        if(this.nodePos[y]){
            while(true){
                if(this.nodePos[y][x]){
                    x += 1
                } else {
                    newVertex['left'] = `${150*x + 50}px`
                    newVertex['pos'] = [x,y]
                    this.nodePos[y][x] = newVertex
                    break
                }
            }
        } else {
            this.nodePos[y] = []
            this.nodePos[y][x] = newVertex
        }
        this.nodeList.push(newVertex)
        this.addPath(this.currentItemTarget,newVertex)
        this.currentItemTarget = newVertex
        this.resetActivate(newVertex)
        this.calcModelId()
    },
    // 修改样式
    resetActivate:function(target){
        d3.selectAll(".history-item.active").classed('hni-node-default-border',true).classed('active',false)
        d3.select(`#${target['uid']}`).classed('hni-node-default-border',false).classed('active',true)
    },
    // 修改当前状态
    changeState:function(target){
        this.currentItemTarget = target
        this.resetActivate(target)
        this.setKeepTag({"keep":"2","dataRoute":"","structureRoute":`${target.ancestor}`})
        this.calcModelId()
    },
    // 模型计数
    calcModelId:function(){
        this.modelAmount += 1
    },
    // 添加连线
    addPath:function(from,to){
        let newLine = {}
        newLine['uid'] = `${from['uid']}_${to['uid']}`
        newLine['from_top'] = from['top']
        newLine['from_left'] = from['left']
        newLine['to_top'] = to['top']
        newLine['to_left'] = to['left']
        this.lineList.push(newLine)
    }
}

export default method;