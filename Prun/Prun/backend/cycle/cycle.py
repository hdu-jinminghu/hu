'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-04-17 20:58:09
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .control_reader import *
def set_cycle_data(request):
    job = request.GET.get('job')
    cycle = request.GET.get('cycle')

    change_control(job ,cycle)
    return "successful"
    # data = data_read(job)
    # return data
