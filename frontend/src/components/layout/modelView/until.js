
//生成指定长度的唯一ID
export function IDGenerator() {
    let i = 1;
    let n = new Date(); 
    let c = n.getTime()
    // console.log(myDate.getTime())
    function generator(type,from=undefined,to=undefined){
        let myDate = new Date(); 
        if(type=="node"){
            i+=1;
            // return `node${i}`;
            return `node${(myDate.getTime()-c).toString(16)}`;
        } else {
            return `${from}-${to}`;
        }
    }
    return generator;
}