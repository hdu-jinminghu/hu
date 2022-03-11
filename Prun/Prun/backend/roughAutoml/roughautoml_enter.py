'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2022-01-24 14:15:41
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .roughauto_graph_reader import *
def roughautoml_executor(request):
    postBody  = request.body
    postBody = json.loads(postBody)
    graph = postBody["graph"]
    tol = postBody["tol"]
    moduleAble = postBody["moduleAble"]
    selectArea = postBody["selectArea"]
    automlM = postBody["automlM"]
    dataset = postBody["dataset"]
    lossFc = postBody["lossFc"]
    epoch = postBody["epoch"]
    obj = {
        "graph":graph,
        "moduleAble":moduleAble,
        "selectArea":selectArea,
        "automlM":automlM,
        "epoch":epoch,
        "tol":tol,
        "dataset":dataset,
        "lossFc":lossFc
    }
    roughautoml(obj)
    return "success"
