'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-12-10 09:58:07
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .auto_graph_reader import *
def get_automl_graph_data(request):
    model_id = request.GET.get('id')
    res = automl_graph_reader(model_id)
    return res
    # data = data_read(job)
    # return data
