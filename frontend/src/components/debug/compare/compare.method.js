import * as d3 from 'd3'
const methods = {
    linechart:function() {
        let {padding,limitVal,compareData,width,height,drawLine,index} = this
        let [minstep,maxstep] = limitVal(compareData,"step")
        d3.select(".compareScalar").select("svg").remove()
        var svg = d3.select(".compareScalar").append("svg").attr("width",width).attr("height",height)
        var xScale = d3.scaleLinear()
            .domain([minstep,maxstep])
            .range([0, width - padding.left - padding.right])
        
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
                .scale(xScale)
                .ticks(10)
            )
        drawLine(svg,index,xScale)
    },
    limitVal:function(val,index) {
        let data = []
        for(let id in val){
            data = data.concat(val[id][index])
        }
        data = data.map(parseFloat)
        data = data.sort(function(a,b){return a-b})
        return [data[0],data[data.length-1]]
    },
    drawLine:function(svg,index,xScale) {
        let {padding,limitVal,compareData,width,height} = this
        let [minVal,maxVal] = limitVal(compareData,index)
        var yScale = d3.scaleLinear()
            .domain([maxVal,minVal])
            .range([0, height - padding.top - padding.bottom])
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
                .scale(yScale)
                .ticks(10)
            )

        const lineFunction = d3
            .line()
            .x(function(d) {
            return xScale(parseInt(d[1]))
            })
            .y(function(d) {
            return yScale(parseFloat(d[0]))
            })
        
        let data = {}

        for(let i in compareData){
            data[i] = []
            for(let j in compareData[i]["step"]){
                let item = []
                item[0] = compareData[i][index][j]
                item[1] = compareData[i]["step"][j]
                item[2] = compareData[i]["color"]
                data[i].push(item)
            }
        }
        for(let i in data){
            const pathg = svg.append('g')
            pathg
            .selectAll('path')
            .data([data[i]])
            .enter()
            .append('g')
            .append('path')
            .attr(
                'transform',
                'translate(' + padding.left + ',' + padding.top + ')'
            )
            .attr('fill', 'none')
            .attr('stroke',data[i][0][2])
            .attr('d', function(d) {
                return lineFunction(d)
            })
        }

    },
    changeActivate(e){
        if(e == this.index){
            return
        } else {
            switch (e){
                case "loss":
                    d3.select(".acc").classed("selected",false);
                    d3.select(".loss").classed("selected",true);
                    break
                case "acc":
                    d3.select(".acc").classed("selected",true);
                    d3.select(".loss").classed("selected",false);
                    break
            }
            this.index = e;
        }
    }
}

export default methods
