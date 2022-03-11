import * as d3 from 'd3'
const methods = {
    update:function(){
        this.fetchTestData({})
    },
    predic_handler:function(){
        this.acc = 0
        this.total = 0
        for(let i = 0 ; i<this.predict.length; i+=1){
            if(this.predict[i][0] == this.predict[i][1]){
                d3.select(`#image${i}`).select(`.image`).classed("truth",true).classed("falth",false);
                this.acc += 1 
            } else {
                d3.select(`#image${i}`).select(`.image`).classed("truth",false).classed("falth",true);
            }
            this.total += 1
        }
    }
}
export default methods;
