'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-12-10 21:08:05
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
import json
import os
import json
import trace
from Prun.backend.utils import getPath,getFileSize
def automl_reader():

    logpath = getPath("Prun/automl")

    acc = []
    loss = []
    folder = []
    data = []
    nml = len(os.listdir(logpath))
    for i in range(1,nml):
        datapath = "{}/{}/performance.json".format(logpath,i)
        modelpath = "{}/{}/parameter/".format(logpath,i)
        try:
            size = getFileSize(modelpath)
            with open(datapath, 'r') as f:
                scalar = json.load(f)
                acc.append(scalar["acc"])
                loss.append(scalar["loss"])
                folder.append(i)
                data.append([scalar["acc"],"%.2f" % (scalar["loss"]),size,i])
        except Exception as e:
            trace.Trace()

    data.sort(key=lambda x:x[0],reverse=True)
    
    return data

