'''
Author: your name
Date: 2021-04-08 15:17:46
LastEditTime: 2021-08-17 22:37:59
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\control\change_control_data.py
'''
def change_control(request):
    job = request.GET.get("job")
    readtag = request.GET.get("readtag")
    modeltype = request.GET.get("modeltype")
    tag = request.GET.get("tag")
    cycle = request.GET.get("cycle")
    paramConq = request.GET.get("paramConq")
    nodeId = request.GET.get("nodeId")
    monitorList = request.GET.get("monitorList")
    appendix = request.GET.get("appendix")
    prunList = request.GET.get("prunList")
    keep = request.GET.get("keep")
    structPath = request.GET.get("structPath")
    dataPath = request.GET.get("dataPath")
    dropout = request.GET.get("dropout")
    batchsize = request.GET.get("batchsize")
    trainCycle = request.GET.get("trainCycle")
    controldata = "@".join([readtag,modeltype,tag,cycle,paramConq,nodeId,monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle])
    # controldata = readtag + '@' + modeltype + '@' + tag + '@' + cycle + '@' + paramConq + '@' + nodeId + '@' + monitorList + '@' + appendix + '@' + prunList
    path = "Prun/data/{}/control.txt".format(job)
    
    f = open(path, 'w')
    f.write(controldata)
    f.close()
    
    return {"controldata":controldata}