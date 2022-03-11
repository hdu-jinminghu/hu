import * as d3 from 'd3'

const methods = {
    linechart:function() {
        const acc = this.acc
        const loss = this.loss
        const step = this.step
        const breakpoints = this.breakpoints
        const xmin = parseInt(step[0])
        const xmax = parseInt(step[step.length - 1])
        const accmin = d3.min(acc,function(d){return parseFloat(d)})
        const accmax = d3.max(acc,function(d){return parseFloat(d)})
        const lossmin = d3.min(loss,function(d){return parseFloat(d)})
        const lossmax = d3.max(loss,function(d){return parseFloat(d)})

        const padding = { top: 10, right: 50, bottom: 20, left: 50 }
        d3.select("#scalar").selectAll("svg").remove()
        var svg = d3.select("#scalar").append("svg").attr("width",this.width).attr("height",this.height)
        var xScale = d3.scaleLinear()
                        .domain([xmin,xmax])
                        .range([0, this.width - padding.left - padding.right])

        var accScale = d3.scaleLinear()
                        .domain([accmax,accmin])
                        .range([0, this.height - padding.top - padding.bottom])
        var lossScale = d3.scaleLinear()
                        .domain([lossmax,lossmin])
                        .range([0, this.height - padding.top - padding.bottom])
        svg
          .append('g')
          .attr('class', 'axis')
          .attr(
            'transform',
            'translate(' + padding.left + ',' + (this.height - padding.bottom) + ')'
          )
          .call(
            d3
              .axisBottom()
              .scale(xScale)
              .ticks(10)
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
              .scale(accScale)
              .ticks(10)
          )
        svg
          .append('g')
          .attr('class', 'lossaxis')
          .attr(
            'transform',
            'translate(' + (this.width-padding.right) + ',' + (padding.top) + ')'
          )
          .call(
            d3
              .axisRight()
              .scale(lossScale)
              .ticks(10)
          )
        const accLineFunction = d3
          .line()
          .x(function(d) {
            return xScale(parseInt(d[1]))
          })
          .y(function(d) {
            return accScale(parseFloat(d[0]))
          })

        const lossLineFunction = d3
          .line()
          .x(function(d) {
            return xScale(parseInt(d[1]))
          })
          .y(function(d) {
            return lossScale(parseFloat(d[0]))
          })
        var accData = []
        for(var i = 0; i<acc.length; i+=1) {
          accData.push([acc[i], step[i]])
        }
        var lossData = []
        for(var i = 0; i<loss.length; i+=1) {
          lossData.push([loss[i], step[i]])
        }
        const accpathg = svg.append('g')

        accpathg
          .selectAll('path')
          .data([accData])
          .enter()
          .append('g')
          .append('path')
          .attr(
            'transform',
            'translate(' + padding.left + ',' + padding.top + ')'
          )
          .attr('fill', 'none')
          .attr('stroke',"blue")
          .attr('d', function(d) {
            return accLineFunction(d)
          })
        const losspathg = svg.append('g')
        losspathg
          .selectAll('path')
          .data([lossData])
          .enter()
          .append('g')
          .append('path')
          .attr(
            'transform',
            'translate(' + padding.left + ',' + padding.top + ')'
          )
          .attr('fill', 'none')
          .attr('stroke',"green")
          .attr('d', function(d) {
            return lossLineFunction(d)
          })
        const breakpointsaccg = svg.append('g')
        breakpointsaccg
            .selectAll('circle')
            .data(breakpoints)
            .enter()
            .append('g')
            .append('circle')
            .attr(
              'transform',
              'translate(' + padding.left + ',' + padding.top + ')'
            )
            .attr("cx",function(d){
              return xScale(step[d])
            })
            .attr("cy",function(d){
              return accScale(acc[d])
            })
            .attr("r","3")
            .style("fill","blue")

        const breakpointslossg = svg.append('g')
        breakpointslossg
            .selectAll('circle')
            .data(breakpoints)
            .enter()
            .append('g')
            .append('circle')
            .attr(
            'transform',
            'translate(' + padding.left + ',' + padding.top + ')'
            )
            .attr("cx",function(d){
            return xScale(step[d])
            })
            .attr("cy",function(d){
            return lossScale(loss[d])
            })
            .attr("r","3")
            .style("fill","green")
    },
}

export default methods