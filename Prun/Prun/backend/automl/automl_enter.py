'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-12-10 20:43:30
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .auto_graph_reader import *
def automl_executor(request):
    depth = request.GET.get('depth')
    epoch = request.GET.get('epoch')
    tol = request.GET.get('tol')
    acc = request.GET.get('acc')
    loss = request.GET.get('loss')
    print(depth,epoch,tol,acc,loss)
    return "success"
    # data = data_read(job)
    # return data
