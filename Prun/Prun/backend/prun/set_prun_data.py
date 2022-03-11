'''
Author: your name
Date: 2021-04-21 16:17:31
LastEditTime: 2022-01-10 15:05:24
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\prun\set_prun_data.py
'''
import json
from .setdata import change_control
def set_prun_data(request):
    postBody  = request.body
    postBody = json.loads(postBody)
    job = postBody["job"]
    prunList = postBody["prunList"]
    conv1 = postBody["conv1"]
    bn2d = postBody["bn2d"]
    conv2 = postBody["conv2"]
    change_control(job, prunList, conv1, bn2d, conv2)
    return prunList

