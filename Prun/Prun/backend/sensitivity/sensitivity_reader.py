'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2022-02-10 15:21:46
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
def sensitivity_read(job,id,step):
    # path = "Prun/data/{}/__cache__/data/result_{}.npz".format(job, step)
    
    controlDir = "Prun/data/{}/control.txt".format(job)
    dataPath = None
    with open(controlDir,"r") as f:
        controlData = f.readline().strip()
        li = controlData.split("@")
        dataPath = li[11]
    path = dataPath + "/" + "result_{}.npz".format(step)
    
    r = np.load(path)
    # weightId = id + '.weight'
    # gradId = id + '.weight_grad'
    weightId = id
    gradId = id + '_back'
    weight = r[weightId]
    grad = r[gradId]
    
    # absGrad = np.abs(grad)
    mul = weight * grad
    s = np.sum(mul,axis=(0,2,3))
    # print(s.shape)
    # s = np.sum(absGrad,axis=(1,2,3))
    # range_ = np.max(s) - np.min(s)
    # s = (s - np.min(s))/range_
    # s = (s)/range_
    s = s.tolist()
    
    return {"sensitivity":s,"id":id,"step":step}
    