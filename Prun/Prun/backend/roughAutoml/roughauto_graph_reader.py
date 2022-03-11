'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2022-01-24 14:20:38
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
from .template import *
from .gModule import *
def roughautoml(obj):
    # with open("model.json","w") as f:
    #     json.dump(obj,f)
    
    holderPlace = obj['automlM']
    skelen = obj['graph']
    # with open("autoModule.json","r") as f:
    #     holderPlace = json.load(f)

    # with open("graph.json","r") as f:
    #     skelen = json.load(f)

    f = Factory(LEVEL_0, LEVEL_1, skelen, holderPlace,int(obj["epoch"]))
    f.initPopulation()
    for i in range(int(obj["tol"])):
        f.ga()
        

