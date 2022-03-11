'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-10-18 16:47:49
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
from Prun.backend.utils import *
def biasGrad_read(job ,id, tag, index,npzPath):
    
    if tag == "contrast":
        data = searchDataPath("bias_grad",job,id,npzPath)
        return data
    
    
    loglist = None
    logDir = "Prun/data/{}/__cache__/logList.txt".format(job)
    controlDir = "Prun/data/{}/control.txt".format(job)
    dataPath = None
    with open(logDir, "r") as f:
        loglist = f.readlines()
    # 更新
    # if tag == "update" or tag == "contrast":
    #     if int(index) < len(loglist) - 1:
    #         index = len(loglist) - 2
    #     else:
    #         return {"tag":"continue","index":index}
    if tag == "update":
        if int(index) < len(loglist) - 1:
            index = len(loglist) - 2
        else:
            return {"tag":"continue","index":index}
        
    # if tag == "contrast" and int(index) >= len(loglist) - 1:
    #     return {"tag":"continue","index":index}
    
    if tag == "current":
        index = int(index) - 1
    
    dir = loglist[int(index)+1][:-1]
    with open(controlDir,"r") as f:
        controlData = f.readline().strip()
        li = controlData.split("@")
        dataPath = li[11]
    path = dataPath+ '/' + dir
    r = np.load(path)
    try:
        v = r[id + '.bias_grad']
        shape = v.shape
        v = v.reshape(-1,1).tolist()
        # if tag == "contrast":
        #     v = contrast(job,id,index+1)
        #     v = v.reshape(-1,1).tolist()
        step = r["step"].tolist()
        pos = splitP(v)
        return {"biasGrad":v,"shape":shape,"step":step,"index":int(index)+1,"tag":"success","op":tag,"split":pos}
    except Exception:
        return {"biasGrad":"none","index":int(index)+1,"tag":"success","op":tag}

# def contrast(job, id, index):
#     # 从index开始向上寻找5个step
#     loglist = None
#     logDir = "Prun/data/{}/__cache__/logList.txt".format(job)
#     with open(logDir, "r") as f:
#         loglist = f.readlines()
#     store = []
#     for i in range(5):
#         try:
#             dir = loglist[int(index) - i][:-1]
#             path = "Prun/data/{}/__cache__/data/".format(job) + dir
#             r = np.load(path)
#             v = r[id + '.bias_grad']
#             store.append(v)
#         except Exception:
#             continue
#     tol = store[0]
#     for data in store[1:]:
#         tol += data
#     average = tol/len(store)
#     var = 0
#     for data in store:
#         var = (data-average)*(data-average)
#     var = var/(len(store)*1.0000000000)
#     return var
