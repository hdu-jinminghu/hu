
//生成指定长度的唯一ID
export function IDGenerator() {
    let i = 1;
    function generator(type,from=undefined,to=undefined){
        if(type=="node"){
            i+=1;
            return `node${i}`;
        } else {
            return `${from}-${to}`;
        }
    }
    return generator;
}