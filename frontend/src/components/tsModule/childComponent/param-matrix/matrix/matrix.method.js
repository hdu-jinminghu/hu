/*
 * @Author: your name
 * @Date: 2021-11-19 20:31:25
 * @LastEditTime: 2021-11-19 20:35:25
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: \frontend\src\components\layout\childComponent\param-matrix\matrix\matrix.method.js
 */
import * as d3 from 'd3'

const methods = {
    // canvas方法绘制
    drawMatrix:function(){
        const paramData = this.paramData[this.paramData['type']]
        const shape = this.paramData["shape"]
        const channels = shape[0]
        var kernelSize = 0
        if(shape.length == 4){
            kernelSize = shape[1] * shape[2] *shape[3]
        } else {
            // 偏置设置为1
            kernelSize = 1
        }
        var channelData = []
        var max = -Infinity
        var min = Infinity
        this.longSide = 5
        const id = this.id
        // 清除canvas内容
        if (document.getElementById(`${id}`) == null) {
            return
        }
        var canvas2d = document.getElementById(`${id}`).getContext('2d')
        
        document.getElementById(`${id}`).width = 0
        
        document.getElementById(`${id}`).width = d3.select(`#${id}`).property("scrollWidth")
        document.getElementById(`${id}`).height = d3.select(`#${id}`).property("scrollHeight")
        if(shape.length == 4){
            for(var i = 0;i<channels;i+=1) {
                channelData.push([])
                for(var j = 0;j<shape[1];j+=1) {
                    for(var k = 0;k<shape[2];k+=1) {
                        for(var l = 0;l<shape[3];l+=1) {
                            channelData[i].push(paramData[i][j][k][l])
                            if (paramData[i][j][k][l] > max) {
                                max = paramData[i][j][k][l]
                            }
                            if (paramData[i][j][k][l] < min) {
                                min = paramData[i][j][k][l]
                            }
                        }
                    }
                }
            }
        } else {
            for(var i = 0;i<channels;i+=1) {
                channelData.push([])
                for(var j = 0;j< 1;j+=1) {
                    channelData[i].push(paramData[i][j])
                    if (paramData[i][j] > max) {
                        max = paramData[i][j]
                    }
                    if (paramData[i][j] < min) {
                        min = paramData[i][j]
                    }
                }
            }
        }
        this.valuescale = d3.scaleLinear().domain([min, max]).range([3, 103])
        if(this.top != -99) {                
            max = this.top
        }
        if(this.bottom != -99) {                
            min = this.bottom
        }

        this.channelData = channelData
        const colorLinear = d3.scaleLinear().domain([min, (min + max) / 2, max]).range(this.rectColor)
        this.maxVal = max.toFixed(2)
        this.minVal = min.toFixed(2)
        // 绘制单个小正方形
        function drawRect(i,j,x,y,width,height,obj) {
            if (channelData[i][j]>max || channelData[i][j]<min){
                obj.fillStyle = '#eeeeee'
            } else {
                obj.fillStyle = colorLinear(channelData[i][j])
            }
            obj.fillRect(x,y,width,width)
        }
        // 将一个卷积绘制为一行
        function mergeSmallRect(i,j,size,x,y,width,height,obj) {
            for(var i_ = 0;i_<size;i_+=1) {
                var x_ = x + i_*width
                drawRect(i,i_,x_,y,width,height,obj)
            }
        }
        // 绘制卷积核
        function drawMConv(i,j,n,size,x,y,width,height,obj) {
            for(var i_=0;i_<n;i_+=1) {
                var y_ = y + i_*height
                mergeSmallRect(i_,j,size,x,y_,width,height,obj)
            }
        }
        this.longSide = this.longSide * this.rectScale
        drawMConv(this.initX,this.initY,channels,kernelSize,0,0,this.longSide,this.longSide,canvas2d)
        this.CanvasRectMouseOperator()
        this.barFunction()

    },
    CanvasRectMouseOperator() {
        const that = this
        const Id = this.id
        function onMouseWheelFunc(e) {
            if (e.wheelDelta < 0) { // 缩小
            that.rectScale *= 0.99
            that.drawMatrix()
            } else { // 放大
            that.rectScale *= 1.01
            that.drawMatrix()
            }
        }
        function onMouseMoveFunc(e) {
            if (that.tag == 1) {
            const currentX = e.screenX
            const currentY = e.screenY
            const moveX = currentX - that.startX
            const moveY = currentY - that.startY
            d3.select(`#${Id}`).style("transform","translate("+(moveX+that.xCoor)+"px,"+(moveY+that.yCoor)+"px)")
            }
        }

        function onMouseDownFunc(e) {
            const str = d3.select(`#${Id}`).style('transform')
            var xCoor = 0
            var yCoor = 0
            if (str!="none") {
            var tmp = str.substring(str.indexOf('(') + 1, str.indexOf(')'))
            tmp = tmp.replace(/px/g,"").split(',')
            xCoor = tmp[0]
            yCoor = tmp[1]
            }
            that.xCoor = parseFloat(xCoor)
            that.yCoor = parseFloat(yCoor)
            that.tag = 1
            that.startX = e.screenX
            that.startY = e.screenY
            const layerX = e.layerX
            const layerY = e.layerY
            const x = parseInt((layerX - xCoor) / that.longSide)
            const y = parseInt((layerY - yCoor) / that.longSide)
            // 数值
            that.digit = that.channelData[y][x]
        }
        function onMouseUpFunc(e) {
            that.tag = 0
        }
        function onMouseLeaveFunc(e) {
            // that.setScrollTag(1)
            that.tag = 0
        }
        function onMouseOutFunc(e) {
            // that.setScrollTag(1)
            that.tag = 0
        }
        function onMouseOverFunc(e) {
            // that.setScrollTag(0)
        }
        document.getElementById(`${Id}`).onmousewheel = onMouseWheelFunc
        document.getElementById(`${Id}`).onmousemove = onMouseMoveFunc
        document.getElementById(`${Id}`).onmousedown = onMouseDownFunc
        document.getElementById(`${Id}`).onmouseup = onMouseUpFunc
        document.getElementById(`${Id}`).onmouseleave = onMouseLeaveFunc
        document.getElementById(`${Id}`).onmouseout = onMouseOutFunc
        document.getElementById(`${Id}`).onmouseover = onMouseOverFunc
    },
    tackleString:function(id) {
        var new_id = id.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\)/g, '\\)').replace(/\./g, '\\.')
        return new_id
    },
    barFunction:function(){
        var self = this
        var gradient = d3.select(`#${this.id}legend${this.paramData['type']}grad1`)
        var bottomBar = d3.select(`#${this.id}legend${this.paramData['type']}bottom`)
        var topBar = d3.select(`#${this.id}legend${this.paramData['type']}top`)
        bottomBar.on('mouseover', function _nonName() {
            d3.select(this).style('cursor', 'e-resize')
        }).call(
            d3.drag().on('drag', function _nonName() {
                d3.select(this).style('cursor', 'e-resize')
                if (d3.event.x >= self.topX-3  || d3.event.x <= 0.00001) self.bottomX = 0
                else  self.bottomX= parseFloat(d3.event.x)
                d3.select(this).attr('x',self.bottomX)
                gradient.attr('x', self.bottomX+3).attr("width",self.topX-3-self.bottomX)
            })
            .on('end', function _nonName() {
                self.bottom = self.valuescale.invert(self.bottomX)
                self.minVal = self.bottom.toFixed(2)
                self.drawMatrix()
            }),
        )
        topBar.on('mouseover', function _nonName() {
            d3.select(this).style('cursor', 'e-resize')
        }).call(
            d3.drag().on('drag', function _nonName() {
                d3.select(this).style('cursor', 'e-resize')
                if (d3.event.x >= 103  || d3.event.x <= self.bottomX+3) self.topX = 103
                else  self.topX= parseFloat(d3.event.x)
                d3.select(this).attr('x',self.topX)
                gradient.attr("width",self.topX-3-self.bottomX)
            })
            .on('end', function _nonName() {
                self.top = self.valuescale.invert(self.topX)
                self.maxVal = self.top.toFixed(2)
                self.drawMatrix()
            }),
        )
    }
}
export default methods;