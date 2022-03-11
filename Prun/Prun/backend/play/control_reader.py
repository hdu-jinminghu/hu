'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2022-01-10 10:51:51
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
import json
def change_control(job,playTag):
    path = "Prun/data/{}/control.txt".format(job)
    # f = open(path, 'r')
    # controldata = f.readline()
    
    # f.close()
    controldata = None
    while True:
        with open(path, 'r') as f:
            controldata = f.readline()
        if controldata:
            break
    [readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle] = controldata.split('@')
    controldata = "@".join([readtag, modeltype, playTag, cycle, paramConq, nodeId, monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle])
    # controldata = readtag + '@' + modeltype + '@' + playTag + '@' + cycle + '@' + paramConq + '@' + nodeId + '@' + monitorList + '@' + appendix + '@' + prunList
    with open(path, "w") as f:
        f.write(controldata)
    
    return "successful"

