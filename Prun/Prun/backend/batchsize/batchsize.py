'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-08-18 16:11:57
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .control_reader import *
def set_batchsize_data(request):
    job = request.GET.get('job')
    batchsize = request.GET.get('batchsize')

    change_control(job ,batchsize)
    return "successful"
    # data = data_read(job)
    # return data
