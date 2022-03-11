'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-08-18 16:17:59
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
def change_control(job,dropout_):
    path = "Prun/data/{}/control.txt".format(job)
    f = open(path, 'r')
    controldata = f.readline()
    [readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle] = controldata.split('@')
    f.close()
    controldata = "@".join([readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList,appendix,prunList,keep,structPath,dataPath,dropout_,batchsize,trainCycle])
    # controldata = readtag + '@' + modeltype + '@' + tag + '@' + cycle_ + '@' + paramConq + '@' + nodeId + '@' + monitorList + '@' + appendix + '@' + prunList
    with open(path, "w") as f:
        f.write(controldata)
    
    return "successful"

