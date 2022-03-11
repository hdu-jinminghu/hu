'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-10-03 22:46:43
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .data_reader import *
def get_trainData(request):
    job = request.GET.get('job')
    dPath = request.GET.get('dPath')
    color = request.GET.get('color')

    data = getdata(job ,dPath,color)
    return data
    # data = data_read(job)
    # return data
