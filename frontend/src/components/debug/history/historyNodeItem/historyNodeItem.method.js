import * as d3 from 'd3'

const method = {
    bubbleInfo:function(){
        this.dealgraph({"op":"read","uid":this.node["uid"]})
        this.setLr(this.node['attrs']['lr'])
        this.setBatch(this.node['attrs']['batch'])
        this.$emit("trigerInfo",this.node)
    },
    onContextmenu() {
        this.$contextmenu({
            items: [{
                label: '对比',
                disabled: false,
                icon: "",
                onClick: () => {
                    this.addTag()
                }
            }],
            event,
            customClass: 'custom-class',
            zIndex: 9999,
            minWidth: 180
        })
    },
    addTag:function(){
        if(this.markStyle['backgroundColor'] != 'transparent'){
            this.getCompareColor[this.markStyle['backgroundColor']] = false
            this.markStyle['backgroundColor'] = 'transparent'
            this.delTrainData(this.node.ancestor)
            return
        }
        for(let color in this.getCompareColor){
            if(!this.getCompareColor[color]){
                this.markStyle['backgroundColor'] = color
                this.getCompareColor[color] = true
                this.fetchTrainData({"dPath":this.node.ancestor,"color":color})
                break
            }
        }
    },
    showFullOp(e){
        d3.select(e.target)
    },
    reset(){

    }
}

export default method;