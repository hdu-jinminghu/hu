/*
 * @Author: your name
 * @Date: 2021-12-06 12:01:13
 * @LastEditTime: 2022-01-27 17:51:24
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: \frontend\src\components\layout\childComponent\listPanel\listPanel.methods.js
 */
import * as d3 from 'd3'
import dagreD3 from 'dagre-d3/dist/dagre-d3'
const methods = {
    // 模型勾选
    check_model:function(e,model_id){
        d3.selectAll(".check_box").classed("checked",false);
        d3.select(e.target).classed("checked",true);
        this.fetchAutomlModelGraph({"id":model_id})
    },
    // 表格排序
    sortModel:function(sort_key){
        this.setSortKey(sort_key)
        const keys = ["sort-acc","sort-loss","sort-size"];
        this.model_list.sort(function(a, b){return parseFloat(b[sort_key])-parseFloat(a[sort_key])});
        for(let key in keys){
            if(key == sort_key){
                d3.select(`.${keys[key]}`).classed("sort-active",true).classed("sort-deactive",false);
            } else {
                d3.select(`.${keys[key]}`).classed("sort-active",false).classed("sort-deactive",true);
            }
        }
    },
    // 图节点布局
    layout:function(graph){
        var g = new dagreD3.graphlib.Graph()
            .setGraph({ranksep: 30})
            .setDefaultEdgeLabel(function() {
              return {}
            })
        graph["nodeList"].forEach((v,index)=>{
            g.setNode(v.id,{"label":v.id,"index":index})
        })
        graph["lineList"].forEach((e,index)=>{
            g.setEdge(e.from, e.to,{ 'id': e.id, 'label': e.id, style: "fill:none;stroke:#333"})
        })
        g.nodes().forEach((v)=>{
            
            const node = g.node(v)
            node.width = 200 // 节点长度
            node.height = 38 //  节点高度
        })
        dagreD3.dagre.layout(g);

        g.nodes().forEach((v)=>{
            const node = g.node(v)
            graph["nodeList"][node["index"]]["top"] = `${node["y"]}px`;
            graph["nodeList"][node["index"]]["left"] = `${node["x"]}px`;
        })
    },
    fetchAutomlList(){
        d3.select(".refresh").classed(".refresh-run",true)
        this.fetchAutomlData({});
    },
    automlProcessExec(){
        this.automlBegin = !this.automlBegin
        this.$nextTick(()=>{
            if(this.automlBegin){
                this.automlProcess(this.config)
            }
        })
    }
}

export default methods;