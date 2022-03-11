'''
Author: your name
Date: 2021-03-29 09:40:24
LastEditTime: 2021-04-08 15:15:40
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \Prun\Prun\backend\scalar_provider\scalar_provider.py
'''

from .control_reader import *
def get_contorl_data(request):
    job = request.GET.get("job")
    data = data_read(job)
    return data
