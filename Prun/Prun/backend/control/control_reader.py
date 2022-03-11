'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-08-17 22:38:15
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
def data_read(job):
    path = "Prun/data/{}/control.txt".format(job)
    f = open(path, 'r')
    controldata = f.readline()
    [readtag, modeltype, tag, cycle, paramConq, nodeId, monitorList,appendix,prunList,keep,structPath,dataPath,dropout,batchsize,trainCycle] = controldata.split('@')
    f.close()
    
    return {"readtag":readtag, "modeltype":modeltype, "tag":tag, "paramConq":paramConq, "nodeId":nodeId,"cycle":cycle,"monitorList":monitorList,"appendix":appendix,"prunList":prunList,"keep":keep,"structPath":structPath,"dataPath":dataPath,"dropout":dropout,"batchsize":batchsize,"trainCycle":trainCycle}

