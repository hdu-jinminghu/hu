'''
Author: your name
Date: 2021-03-29 09:39:17
LastEditTime: 2021-11-09 14:45:11
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\data_reader.py
'''
import json
import time

from .process import process

processUid = None

def modelTxtUrlReader(request):
    postBody  = request.body
    postBody = json.loads(postBody)
    job = postBody["job"]
    modelTxt = postBody["modelTxt"]
    lossFc = postBody["lossFc"]
    dataset = postBody["dataset"]
    g = postBody["g"] # 生成/重新加载
    res = process(job,modelTxt,lossFc,dataset,g)
    return res
    
    

