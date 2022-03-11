import * as d3 from "d3"
const method = {
    changePanel:function(stage){

        d3.selectAll('.activep').classed('activep',false)
        d3.selectAll('.activep-tri').classed('activep-tri',false)

        for(let ele of this.eles[stage]){
            let actiClass = ele.endsWith('stri')?'activep-tri':'activep'
            d3.select(`.${ele}`).classed(actiClass,true)
        }
        this.$router.currentRoute.fullPath != this.process[stage] && (this.$router.push({ path: this.process[stage] }))
    }
}

export default method 