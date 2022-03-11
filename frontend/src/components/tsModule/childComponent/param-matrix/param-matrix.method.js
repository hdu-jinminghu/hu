/*
 * @Author: your name
 * @Date: 2021-11-19 20:04:38
 * @LastEditTime: 2021-11-22 16:43:19
 * @LastEditors: Please set LastEditors
 * @Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 * @FilePath: \frontend\src\components\layout\childComponent\param-matrix\param-matrix.method.js
 */
import * as d3 from 'd3'
const methods = {
    tackleString:function(id) {
        var new_id = id.replace(/\//g, '\\/').replace(/\(/g, '\\(').replace(/\)/g, '\\)').replace(/\)/g, '\\)').replace(/\./g, '\\.')
        return new_id
    },
    changeMatrix:function(val){
        let value = d3.select("#range").property("value");
        this.scrollTag = true;
        let length = this.npzList.length;
        let seg = 5/length;
        let pos = Math.ceil(value/seg);
        this.pos = pos;
        d3.select("#range").property("value",pos*seg);
        console.log(pos)
        if(this.newValue.match(/weight:/)) {
                this.weight({"Id":this.tackle_node,"tag":"contrast","npzPath":this.npzList[pos-1]})
        } else if(this.newValue.match(/weightGrad:/)) {
            this.weightGrad({"Id":this.tackle_node,"tag":"contrast","npzPath":this.npzList[pos-1]})
        } else if(this.newValue.match(/bias:/)) {
            this.bias({"Id":this.tackle_node,"tag":"contrast","npzPath":this.npzList[pos-1]})
        } else if(this.newValue.match(/biasGrad:/)) {
            this.biasGrad({"Id":this.tackle_node,"tag":"contrast","npzPath":this.npzList[pos-1]})
        }
    
    }
}

export default methods;