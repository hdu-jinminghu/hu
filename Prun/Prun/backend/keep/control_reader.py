'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-08-23 11:41:13
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
import json
def change_control(job,keepTag,dataRouteAppdendix,structureRouteAppdendix):
    path = "Prun/data/{}/control.txt".format(job)
    data = None
    with open(path,"r") as f:
        data = f.readline().strip()
    cSegs = data.split("@")
    keep = cSegs[9]
    sPath = cSegs[10]
    dPath = cSegs[11]
    # 保存训练节点
    if keepTag == "1":
        cSegs[9] = "1"
    # 节点重载
    elif keepTag == "2":
        cSegs[9] = "2"
        segs = sPath.split("/")
        length = len(segs)
        for i in range(length-1,-1,-1):
            if "model_" in segs[i]:
                segs.pop()
            else:
                break
        dap = structureRouteAppdendix.split("/")
        for i in dap:
            segs.append("model_{}".format(i))
        cSegs[10] = "/".join(segs)
    # 剪枝复原
    elif keepTag == "3":
        cSegs[9] = "3"
        segs = dPath.split("/")
        segs.pop()
        length = len(segs)
        for i in range(length-1,-1,-1):
            if "model_" in segs[i]:
                segs.pop()
            else:
                break
        dap = dataRouteAppdendix.split("/")
        for i in range(len(dap)-1):
            segs.append("model_{}".format(dap[i]))
        segs.append(dap[-1])
        cSegs[11] = "/".join(segs)
    print(cSegs[11])
    controldata = "@".join(cSegs)
    with open(path, "w") as f:
        f.write(controldata)
    
    return "successful"

