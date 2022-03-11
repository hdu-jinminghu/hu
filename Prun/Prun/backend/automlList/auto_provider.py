'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-12-10 20:26:18
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''
import json
from .auto_reader import *
def get_automl_list_data(request):

    res = automl_reader()
    return res
    # data = data_read(job)
    # return data
