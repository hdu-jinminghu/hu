'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-08-18 16:18:38
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .control_reader import *
def set_trainCycle_data(request):
    job = request.GET.get('job')
    trainCycle = request.GET.get('trainCycle')

    change_control(job ,trainCycle)
    return "successful"
    # data = data_read(job)
    # return data
