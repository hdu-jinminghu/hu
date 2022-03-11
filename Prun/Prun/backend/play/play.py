'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-06-25 10:24:30
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .control_reader import *
def set_playTag_data(request):
    job = request.GET.get('job')
    tag = request.GET.get('tag')

    change_control(job ,tag)
    return "successful"
    # data = data_read(job)
    # return data
