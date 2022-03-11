import * as d3 from "d3"
const method = {
    triger:function(e){
        let attrClass = d3.select(e.path[0]).attr('class')
        let classList = attrClass.split(' ')
        for(let class_ of classList){
            if(this.buttonTypeMap[class_]){
                this.$emit("trigerEvent", this.buttonTypeMap[class_])
                return
            } 
        }
        this.$emit("trigerEvent", 'run')
    }
}

export default method;