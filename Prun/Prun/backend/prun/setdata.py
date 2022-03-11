'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2022-01-10 15:11:28
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
def change_control(job,prunList,conv1, bn2d, conv2):
    path = "Prun/data/{}/control.txt".format(job)
    prunTargetPath = "Prun/data/{}/prunTarget.json".format(job)
    f = open(path, 'r')
    controldata = f.readline()
    [readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList,appendix,prunList_,keep,structPath,dataPath,dropout,batchsize,trainCycle] = controldata.split('@')
    f.close()
    controldata = "@".join([readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle])
    # controldata = readtag + '@' + modeltype + '@' + tag + '@' + cycle + '@' + paramConq + '@' + nodeId + '@' + monitorList + '@' + appendix + '@' + prunList
    with open(path, "w") as f:
        f.write(controldata)
    with open(prunTargetPath, "w") as f:
        json.dump({"conv1":conv1,"bn2d":bn2d,"conv2":conv2},f)
    
    return "successful"