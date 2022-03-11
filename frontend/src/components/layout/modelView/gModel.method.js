const method = {
      gModel:function(){
        console.log("o")
        let graph = this.graph
        if(this.exploreStage.length > 0){
          graph = this.exploreStage[0]
        }
        this.$nextTick(()=>{this.setModelSData([this.modelName,graph,this.lossFc,this.dataset])})
        this.$nextTick(()=>{this.setOriGraph(graph)})
        this.$nextTick(()=>{this.genereModel({"modelTxt":graph,"lossFc":this.lossFc,"dataset":this.dataset,"g":"generator"})})
      },
      nodeMouseOver:function(val){
        this.overNodeId = val
      }
}

export default method