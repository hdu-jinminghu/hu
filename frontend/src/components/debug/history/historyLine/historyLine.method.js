import * as d3 from 'd3'
const method = {
    drawLine:function(){
        let svg = d3.select(`#${this.myline['uid']}`)
        let startX = 70
        let startY = 0
        let endX = parseInt(this.lineStyle['width']) - 70
        let endY = parseInt(this.lineStyle['height'])
        let path = `M${startX} ${startY} L ${startX} ${(startY+endY)/2} L ${endX} ${(startY+endY)/2} L ${endX} ${endY-3}`
        svg.append('path').attr('d',path).attr('fill','none').attr('stroke-width',2).attr('stroke','#2c3e50').attr('marker-end','url(#markerArrow)')
    }
}

export default method;