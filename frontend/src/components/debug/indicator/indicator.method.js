import * as d3 from 'd3'

const methods = {
    drawBubble:function() {
        d3.select(".indicator-section").selectAll("svg").remove()
        const self = this
        const padding = { top: 20, right: 20, bottom: 30, left: 30 }
        const height = this.height * 1
        const width = this.width
        const rank = this.paramData["rank"]
        const sensitivity = this.paramData["sensitivity"]

        const rankMax = d3.max(rank,function(d){return parseFloat(d)})
        const rankMin = d3.min(rank,function(d){return parseFloat(d)})

        const senMax = d3.max(sensitivity,function(d){return parseFloat(d)})
        const senMin = d3.min(sensitivity,function(d){return parseFloat(d)})
        const clearArray = this.clearArray

        clearArray(this.brushed)
        this.percentage = 0
        var svg = d3.select(".indicator-section").append("svg").attr("width",this.width).attr("height",height).attr("id","indi")
        console.log(svg)
        var data = []
        for(var i = 0; i<rank.length; i += 1) {
            var tmp = []
            tmp.push(rank[i])
            tmp.push(sensitivity[i])
            tmp.push(i)
            data.push(tmp)
        }

        const rankLinear = d3.scaleLinear()
            .domain([rankMin, rankMax])
            .range([height - padding.top - padding.bottom, 0])

        const senLinear = d3.scaleLinear()
            .domain([senMin, senMax])
            .range([0, width - padding.left - padding.right])
        // let s = 0
        // let m = senMin
        // for(;m<1;s=s+1){
        //     m = m*10
        // }
        let s = senMin.toPrecision(2)
        s = s.split('-')
        if(s.length == 2){
            s = Number(s[1])
        } else {
            s = Number(s[2])
        }
        svg
            .append('g')
            .attr('class', 'axis')
            .attr(
                'transform',
                'translate(' + padding.left + ',' + (height - padding.bottom) + ')'
            )
            .call(
                d3
                .axisBottom()
                .scale(senLinear)
                .ticks(10)
                // .tickFormat((d,i)=>d.toPrecision(2))
                .tickFormat((d,i)=>(d*Math.pow(10,s)).toFixed(1))
            )
        svg
            .append('g')
            .attr('class', 'accaxis')
            .attr(
                'transform',
                'translate(' + padding.left + ',' + (padding.top) + ')'
            )
            .call(
                d3
                .axisLeft()
                .scale(rankLinear)
                .ticks(10)
                // .tickFormat(d3.format(".3f"))
            )
        
        svg.selectAll("circle").data(data).enter().append("circle").attr("cx",function(d){return padding.left + senLinear(d[1])}).attr("cy",function(d){return (padding.top + rankLinear(d[0]))})
            .attr("r",5).attr("id",function(d){return d[2]})
        self.kernelSize = data.length
        let chengji = svg.append("g").style("transform","translate(95%, 85%)").style("font-family","fangsong").style("font-size","12px");;
        chengji.append("text").html(`e${s}`)
        var brush = d3
            .brush()
            .extent([
            [padding.left, padding.top],
            [(width - padding.left), (height - padding.top)]
            ]).on('end', () => {
               var pos = d3.event.selection
               var brushed = []
               if(pos != null) {
                    var brushed = []
                    var lt = pos[0]
                    var rb = pos[1]
                    var circles = svg.selectAll("circle")["_groups"][0]
                    var length = circles.length
                    for (var i=0; i<length;i+=1) {
                        var circle = d3.select(circles[i])
                        var cx = parseFloat(circle.attr("cx"))
                        var cy = parseFloat(circle.attr("cy"))
                        var index = parseInt(circle.attr("id"))
                        if (cx >= lt[0] && cx <= rb[0] && cy >= lt[1] && cy <= rb[1]) {
                            brushed.push(index)
                        }
                    }
                    
                    for(var i = 0;i<brushed.length;i+=1) {
                        if(self.brushed.indexOf(brushed[i]) < 0) {
                            self.brushed.push(brushed[i])
                        }
                    }
                    self.percentage = self.brushed.length/circles.length * 100
                    
               }
               
            })
        svg.append('g')
            .attr('class', 'brush')
            .call(brush)
    },
    tackleString:function(id) {
        var new_id = id.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\)/g, '\\)').replace(/\./g, '\\.')
        return new_id
    },
    drawDisplay:function(id) {
        d3.select("#displayBrushed").select("g").remove()
        var self = this
        var g = d3.select("#displayBrushed").append("g")
        var brushed = this.brushed
        var width = d3.select("#displayBrushed").property("scrollWidth")
        var max_n = Math.floor((width - 40)/20)
        for(var i = 0;i<brushed.length;i+=1) {
            var row = Math.floor(i / max_n)
            var j = i - row * max_n
            var circleContainer =  g.append("g").attr("transform",`translate(${20*j+20},${20*row + 20})`)
            circleContainer.append("circle").attr("cx",0).attr("cy",0).attr("r",5).attr("id",brushed[i])
            circleContainer.append("circle").attr("cx",0).attr("cy",0).attr("r",10)
                .attr("id",brushed[i]).attr('fill-opacity', 0)
                .on("mouseover",function(u){
                    var uid = d3.select(this).attr("id")
                    var svg = d3.select(".indicator-section").select("svg")
                    var circles = svg.selectAll("circle")["_groups"][0]
                    var length = circles.length
                    for (var j=0; j<length;j+=1) {
                        var circle = d3.select(circles[j])
                        if(circle.attr("id") == uid) {
                            circle.remove()
                            d3.select(".indicator-section").select("svg").append("circle").attr("cx",circle.attr("cx")).attr("cy",circle.attr("cy")).attr("r",circle.attr("r")).attr("fill","#67C23A").attr("id",circle.attr("id"))
                            break
                        }
                    }
                    self.id_ = uid
                })
                .on("mouseout",function(u){
                    var uid = d3.select(this).attr("id")
                    var svg = d3.select(".indicator-section").select("svg")
                    var circles = svg.selectAll("circle")["_groups"][0]
                    var length = circles.length
                    for (var j=0; j<length;j+=1) {
                        var circle = d3.select(circles[j])
                        if(circle.attr("id") == uid) {
                            circle.attr("fill","black")
                            break
                        }
                    }
                })
                .on("dblclick",function(u){
                    var uid = d3.select(this).attr("id")
                    var svg = d3.select(".indicator-section").select("svg")
                    var circles = svg.selectAll("circle")["_groups"][0]
                    var length = circles.length
                    for (var j=0; j<length;j+=1) {
                        var circle = d3.select(circles[j])
                        if(circle.attr("id") == uid) {
                            circle.attr("fill","black")
                            break
                        }
                    }
                    var index = brushed.indexOf(parseInt(uid))
                    
                    brushed.splice(index,1)
                    self.percentage = brushed.length / length * 100
                })
        }
        d3.select("#displayBrushed").style("height",Math.floor(brushed.length/max_n)*20 + 40)
    },
    prun_:function(){
        
        // var self = this
        var brushed = this.brushed
        // this.$emit("opContent","content")
        // this.set_prun_tag()
        // return

        if(brushed.length == 0) {
            return
        } 

        var prunList = JSON.stringify(brushed)
        this.directive_prun({"prunList":prunList})

        var conv1 = this.get_targetVertex["conv1"]
        var bn2d = this.get_targetVertex["bn2d"]
        var conv2 = this.get_targetVertex["conv2"]
        var conv1size = parseInt(conv1["attrs"]["out_channels"])

        conv1["attrs"]["out_channels"] = parseInt(conv1["attrs"]["out_channels"]) - brushed.length
        bn2d["attrs"]["num_features"] = parseInt(bn2d["attrs"]["num_features"]) - brushed.length
        conv2["attrs"]["in_channels"] = parseInt(conv2["attrs"]["in_channels"]) - brushed.length

        var svg = d3.select(".indicator-section").select("svg")
        var circles = svg.selectAll("circle")["_groups"][0]
        var length = circles.length
        for (var j=0; j<length;j+=1) {
            var circle = d3.select(circles[j])
            if(brushed.indexOf(parseInt(circle.attr("id"))) >=0) {
                circle.remove()
            }
        }
        this.kernelSize = length - this.brushed.length

        let content = `${conv1["id"]} (${conv1size}->${conv1size-brushed.length})`
        this.brushed.splice(0,this.brushed.length)
        this.setPrunContent(content)
        this.percentage = 0
        // this.set_prun_tag() // 通知历史模块生成节点
        
    },
    idTransformer:function(id) {
        var id = id.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\]/g, '\\]').replace(/\[/g, '\\[')
        return id
    },
    clearArray:function(arr) {
        arr.splice(arr.length)
    }
}

export default methods;