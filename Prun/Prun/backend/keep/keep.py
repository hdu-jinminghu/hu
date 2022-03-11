'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-08-23 10:06:53
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .control_reader import *
def set_keep_data(request):
    job = request.GET.get('job')
    keepTag = request.GET.get('keep')
    dataRouteAppdendix = request.GET.get('dataRoute')
    structureRouteAppdendix = request.GET.get('structureRoute')
    change_control(job,keepTag,dataRouteAppdendix,structureRouteAppdendix)
    return "successful"
    # data = data_read(job)
    # return data
