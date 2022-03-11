'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-12-13 10:32:59
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
def get_data(job ,id, step):
    # path = "Prun/data/{}/__cache__/data/result_{}.npz".format(job, step)
    controlDir = "Prun/data/{}/control.txt".format(job)
    dataPath = None
    with open(controlDir,"r") as f:
        controlData = f.readline().strip()
        li = controlData.split("@")
        dataPath = li[11]
    path = dataPath + "/" + "result_{}.npz".format(step)
    r = np.load(path)
    v = r[id]
    np.clip(v,a_min=0,a_max=100,out=v)
    # print(v)
    return v
    
def rank(data):
    a = np.amin([200,data.shape[0]])
    b = data.shape[1]
    c = np.array([np.linalg.matrix_rank(data[i,j,:,:]) for i in range(a) for j in range(b)])
    c = c.reshape([a,-1])
    c = np.sum(c,axis=0)
    total = 1.0 * a
    c = c / total
    return c


def rank_read(job ,id, step):
    data = get_data(job ,id, step)
    avg_rank = rank(data)
    return {"rank":avg_rank.tolist(),"id":id, "step":step}
