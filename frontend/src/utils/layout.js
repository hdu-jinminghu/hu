import dagreD3 from 'dagre-d3/dist/dagre-d3'

let utils = {
    layout:function(graph){
        let doubleLayer = ["conv2d","bn2d","linear"]
        var g = new dagreD3.graphlib.Graph()
            .setGraph({ranksep: 40})
            .setDefaultEdgeLabel(function() {
              return {}
            })
        graph["nodeList"].forEach((v,index)=>{
            console.log(v.id)
            g.setNode(v.id,{"label":v.id,"index":index ,"type":v.type})
        })
        graph["lineList"].forEach((e,index)=>{
            console.log(e.from,e.to)
            g.setEdge(e.from, e.to,{ 'id': e.id, 'label': e.id, style: "fill:none;stroke:#333"})
        })

        g.nodes().forEach((v)=>{
            const node = g.node(v)
            console.log(node)
            if(doubleLayer.includes(node.type)){
                node.width = 250 // 节点长度
                node.height = 25 //  节点高度
            } else {
                node.width = 250 // 节点长度
                node.height = 20
            }
        })
        dagreD3.dagre.layout(g);
    
        g.nodes().forEach((v)=>{
            const node = g.node(v)
            graph["nodeList"][node["index"]]["top"] = `${node["y"]}px`;
            graph["nodeList"][node["index"]]["left"] = `${node["x"]}px`;
        })
    }
}

export default utils