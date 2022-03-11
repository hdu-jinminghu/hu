'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-09-14 20:10:16
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .control_reader import *
def set_monitor_data(request):
    postBody  = request.body
    postBody = json.loads(postBody)
    monitorList = postBody["monitorList"]
    job = postBody["job"]
    tag = postBody["tag"]
    change_control(job ,monitorList,tag)
    return postBody
    # data = data_read(job)
    # return data
