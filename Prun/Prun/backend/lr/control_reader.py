'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-08-18 16:52:20
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import numpy as np
import json
def change_control(job,lr):
    path = "Prun/data/{}/control.txt".format(job)
    data = None
    with open(path,"r") as f:
        data = f.readline().strip()
    segs = data.split("@")
    param = segs[4]
    obj = json.loads(param)
    for key in obj.keys():
        obj[key]["attrs"][0]["lr"] = float(lr)
    segs[4] = json.dumps(obj)
    controldata = "@".join(segs)
    with open(path, "w") as f:
        f.write(controldata)
    
    return "successful"

