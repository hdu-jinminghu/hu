'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-10-03 22:46:57
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
def getdata(job,dPath,color):
    lossPath = "Prun/data/"+ job + "/model_" + "/model_".join(dPath.split("/")) + "/loss.txt"
    accPath = "Prun/data/"+ job + "/model_" + "/model_".join(dPath.split("/")) + "/accuracy.txt"
    data = {"dPath":dPath,"acc":[],"loss":[],"step":[]}
    lossdata = None
    accdata = None
    step = []
    acc = []
    loss = []
    with open(lossPath,"r") as f:
        lossdata = f.readlines()
    with open(accPath,"r") as f:
        accdata = f.readlines()
    for i in range(len(lossdata)):
        accTxt_ = accdata[i]
        lossTxt_ = lossdata[i]
        acc_ = accTxt_.split(',')
        loss_ = lossTxt_.split(',')
        step.append(acc_[1][:-1])
        acc.append(acc_[0])
        loss.append(loss_[0])
    
    return {"dPath":dPath,"acc":acc,"loss":loss,"step":step,"color":color}

