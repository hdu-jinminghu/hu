'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-11-09 15:53:20
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
import os
import sys
import multiprocessing
import time
from Prun.backend.utils import getPath
from .train import buildModel

processUid = None

def process(job,modelTxt,lossFc,dataset,g):
    if g == '':
        return {"tag":"success."}
    global processUid
    path = getPath("./Prun/data/model.json")
    with open(path,"w") as f:
        data = json.dumps(modelTxt)
        # print(modelTxt)
        f.write(data)
        time.sleep(0.3)
        
    
    if processUid:
        # 结束旧进程
        print("end process")
        processUid.terminate()
        processUid.join()
        processUid = None
        
        print("start process")
        processUid = multiprocessing.Process(target=buildModel,args=(lossFc,dataset,job,g,))
        processUid.start()
    else:
        print("start process")
        processUid = multiprocessing.Process(target=buildModel,args=(lossFc,dataset,job,g,))
        processUid.start()
    return {"tag":"success"}
