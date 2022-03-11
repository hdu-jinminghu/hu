'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-09-14 20:40:45
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
import json
def change_control(job,monitorList_,drop):
    path = "Prun/data/{}/control.txt".format(job)
    f = open(path, 'r')
    controldata = f.readline()
    [readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle] = controldata.split('@')
    f.close()
    print(tag)
    if drop == "drop":
        ml = json.loads(monitorList)
        for i in range(len(ml)):
            if ml[i] == monitorList_:
                 del ml[i]
                 break
        monitorList_ = json.dumps(ml)
    controldata = "@".join([readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList_,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle])
    # controldata = readtag + '@' + modeltype + '@' + tag + '@' + cycle + '@' + paramConq + '@' + nodeId + '@' + monitorList_ + '@' + appendix+ '@' + prunList
    with open(path, "w") as f:
        f.write(controldata)
    
    return "successful"

