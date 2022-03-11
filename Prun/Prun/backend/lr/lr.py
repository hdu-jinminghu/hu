'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-08-18 16:52:32
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .control_reader import *
def set_lr_data(request):
    job = request.GET.get('job')
    lr = request.GET.get('lr')

    change_control(job ,lr)
    return "successful"
    # data = data_read(job)
    # return data
